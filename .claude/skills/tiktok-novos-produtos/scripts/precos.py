"""Passo 3: calcula o preço de venda TikTok dos SKUs a criar.

Uso: python3 -I precos.py <pasta_lote>

Lê novos.json, refs.json e bling.json ({sku: {preco, custo, situacao, formato, kit, nota}}).
Regras (CLAUDE.md):
- referência = menor entre Shopee (Regra Especial; senão Controle Shopee/Regra Padrão; Tanke: menor com a loja Tanke)
  e Mercado Livre (Clássico; senão Premium);
- margem no preço da referência < 10% -> primeiro preço redondo com 10%;
- sem referência -> primeiro preço redondo com 15%;
- variantes do mesmo produto (mesmo product_id) -> mesmo preço (o maior entre elas);
- a oferta precisa ser menor que o preço original do TikTok (coluna price da exportação):
  se não for, tenta margem de 20%; senão o maior preço redondo abaixo do original com margem >= 10%;
  senão o SKU fica FORA da promoção.
Gera linhas.json (uma por SKU a criar) e imprime o resumo por produto.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import first_m, nice_below, ttm  # noqa: E402

L = sys.argv[1]
novos = json.load(open(f'{L}/novos.json'))
refs = json.load(open(f'{L}/refs.json'))
bl = json.load(open(f'{L}/bling.json'))

orig, prod = {}, {}
for r in novos:
    orig.setdefault(r[10], float(r[9]))
    prod.setdefault(r[10], r[0])

linhas, avisos = [], []
for sk, v in refs.items():
    b = bl.get(sk) or {}
    c, cheio = b.get('custo'), b.get('preco')
    if not c:
        avisos.append(f'{sk} sem custo no Bling: confirme buscando só esse SKU')
        continue
    c = round(float(c), 2)
    shop = v['re'] or v['shp']
    if v['tk'] and (not shop or v['tk'] < shop):
        shop = v['tk']
    rr = [x for x in (shop, v['ml']) if x]
    if rr:
        p, t = round(min(rr), 2), 'igual menor canal'
        if ttm(c, p) < 0.10:
            p, t = first_m(c, 0.10), 'subido p/ MC 10%'
    else:
        p, t = first_m(c, 0.15), 'sem ref (MC 15%)'
    nome = ' '.join(v['name'].split())
    if v['var'] not in ('Padrão', None, ''):
        nome += f" Cor:{v['var']}"
    linhas.append(dict(sku=sk, prod=prod[sk], nome=nome, c=c, p=p, t=t, ml=v['ml'], shp=shop, cheio=cheio,
                       orig=orig[sk], obs=[], fora=False))

# variantes: mesmo preço (o maior do grupo, para todas ficarem com margem >= mínima)
grp = collections.defaultdict(list)
for x in linhas:
    grp[x['prod']].append(x)
for xs in grp.values():
    pm = max(x['p'] for x in xs)
    for x in xs:
        if x['p'] != pm:
            x['p'] = pm
            x['t'] += ' | igualado às variantes'

# oferta < preço original
for x in linhas:
    b = bl.get(x['sku']) or {}
    if b.get('kit'):
        x['obs'].append('Kit: ' + b['kit'])
    if b.get('situacao') == 'I':
        x['obs'].append('Inativo no Bling (custo = preço de custo do cadastro)')
    k = refs[x['sku']]
    if 'aprox' in (k['k_re'], k['k_shp'], k['k_ml']):
        x['obs'].append('Ref. por nome aproximado')
    if x['p'] >= x['orig']:
        p20 = first_m(x['c'], 0.20)
        pb = nice_below(x['orig'])
        if p20 < x['orig']:
            x['p'], msg = p20, f"venda >= preço original R$ {x['orig']:.2f}: ajustado p/ MC 20%"
        elif pb and ttm(x['c'], pb) >= 0.10:
            x['p'], msg = pb, f"venda >= preço original R$ {x['orig']:.2f}: maior preço abaixo dele"
        else:
            x['fora'] = True
            msg = (f"FORA DA PROMOÇÃO: no preço original R$ {x['orig']:.2f} a margem é "
                   f"{ttm(x['c'], x['orig']) * 100:.1f}%")
        x['t'] += ' | ' + msg
        x['obs'].append(msg)
    x['mc'] = round(ttm(x['c'], x['p']), 4)

json.dump(linhas, open(f'{L}/linhas.json', 'w'), ensure_ascii=False)
print(dict(collections.Counter(x['t'].split(' | ')[0] for x in linhas)), '| fora da promoção:',
      [x['sku'] for x in linhas if x['fora']])
for a in avisos:
    print('AVISO', a)
vist = set()
for x in linhas:
    if x['prod'] in vist:
        continue
    vist.add(x['prod'])
    xs = grp[x['prod']]
    flag = ('!' if any(' | ' in y['t'] for y in xs) else ' ') + ('S' if 'sem ref' in x['t'] else ' ') + \
           ('U' if 'subido' in x['t'] else ' ')
    print(f"{flag} {x['nome'].split(' Cor:')[0][:52]:52} n={len(xs)} custo={sorted({y['c'] for y in xs})} "
          f"cheio={x['cheio']} SHP={x['shp']} ML={x['ml']} -> {x['p']} MC {min(y['mc'] for y in xs) * 100:.1f}%")
