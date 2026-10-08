"""Passo 2: procura o preço de referência (Shopee e Mercado Livre) dos SKUs a criar.

Uso: python3 -I refs.py <pasta_lote>

Lê da pasta do lote: novos.json, skus_criar.json e a subpasta refs/ com os get_values salvos:
  refs/regra_especial.json  'Regra Especial Shopee AGO2026'!A1:J3000   (Shopee, referência principal)
  refs/shopee.json          'Controle Anúncios Shopee'!A1:P3000
  refs/regra.json           'Regra Shopee Padrão'!A1:N3000
  refs/tanke.json           'Shopee TANKE'!A1:N3000                   (loja Tanke na Shopee)
  refs/ml.json              'Cálculo de Margem 0203'!A1:L3000         (Mercado Livre)
Essas abas são só lidas, nunca alteradas.

Gera refs.json: {sku: {name, var, re, shp, tk, ml, k_re, k_shp, k_ml}} e lista o que ficou sem referência
ou com nome aproximado.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Index, g, load_values, norm, num  # noqa: E402

L = sys.argv[1]
R = f'{L}/refs'


def idx_simple(path, col_price=9, col_margin=10, skip_obs=None):
    ix = Index()
    for r in load_values(path)[1:]:
        if not str(g(r, 0)).strip():
            continue
        p, m = num(g(r, col_price)), num(g(r, col_margin))
        if not p or m is None:
            continue
        if skip_obs is not None and str(g(r, skip_obs)).strip().lower() in ('sugestão', 'sugestao', 'concorrente'):
            continue
        ix.add(r[0], p)
    return ix


# Regra Especial: linha de produto = nome em A e preço de venda em I (índice 8).
# Se o mesmo nome aparece mais de uma vez com preços diferentes, vale a PRIMEIRA linha
# (critério usado desde o 1º lote) e a duplicidade é avisada no final.
RE = Index()
re_todos = {}
for i, r in enumerate(load_values(f'{R}/regra_especial.json')[1:], start=2):
    p = num(g(r, 8))
    if str(g(r, 0)).strip() and p and str(g(r, 3)).strip():
        RE.add(r[0], p)
        re_todos.setdefault(norm(r[0]), []).append((i, p))

SHP = idx_simple(f'{R}/shopee.json')
RG = idx_simple(f'{R}/regra.json')
TK = idx_simple(f'{R}/tanke.json')

# Mercado Livre: Clássico tem prioridade sobre Premium (coluna D)
ML_C, ML_P = Index(), Index()
for r in load_values(f'{R}/ml.json')[1:]:
    if not str(g(r, 0)).strip():
        continue
    p, m = num(g(r, 9)), num(g(r, 10))
    if not p or m is None or str(g(r, 11)).strip().lower() in ('sugestão', 'sugestao', 'concorrente'):
        continue
    (ML_C if 'CLASS' in str(g(r, 3)).upper() else ML_P).add(r[0], p)

novos = json.load(open(f'{L}/novos.json'))
criar = set(json.load(open(f'{L}/skus_criar.json')))
out, vistos = {}, set()
for r in novos:
    sk, name, var = r[10], r[2], r[7]
    if sk not in criar or sk in out:
        continue
    re_, k1 = RE.find(name)
    shp, k2 = (None, None)
    if not re_:
        shp, k2 = SHP.find(name)
        if not shp:
            shp, k2 = RG.find(name)
    tk = TK.find(name)[0] if 'tanke' in name.lower() else None
    ml, k3 = ML_C.find(name)
    if not ml:
        ml, k3 = ML_P.find(name)
    out[sk] = dict(name=name, var=var, re=re_, shp=shp, tk=tk, ml=ml, k_re=k1, k_shp=k2, k_ml=k3)
    if name not in vistos:
        vistos.add(name)
        o = out[sk]
        if not (re_ or shp or tk or ml):
            print('SEM REF  |', name[:70])
        elif 'aprox' in (k1, k2, k3):
            print('APROX    |', name[:70], '| RE', re_, '| SHP', shp, '| ML', ml, '| TK', tk)
json.dump(out, open(f'{L}/refs.json', 'w'), ensure_ascii=False)
for sk, v in out.items():
    linhas_re = re_todos.get(norm(v['name']), [])
    if len({p for _, p in linhas_re}) > 1 and sk == next(k for k, o in out.items() if o['name'] == v['name']):
        print('DUPLICADO NA REGRA ESPECIAL |', v['name'][:60], '| linhas/preços:', linhas_re, '| usado:', v['re'])
sem = sum(1 for v in out.values() if not (v['re'] or v['shp'] or v['tk'] or v['ml']))
print(f'SKUs: {len(out)} | produtos: {len(vistos)} | sem referência: {sem}')
