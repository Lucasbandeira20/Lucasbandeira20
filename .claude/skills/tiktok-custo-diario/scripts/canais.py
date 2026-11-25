"""Compara o preço do TikTok com Shopee e Mercado Livre (planilha do comercial, só leitura).

Uso: python3 -I canais.py <pasta> "<dd/mm/aaaa>" [anterior.json]
Entrada:
  ctl.json     CONTROLE A1:AH1281 (B nome, C SKU, L preço, M margem, AE preço na PROMOÇÕES)
  ml.json      'Controle Promoção ML'!A1:N (B produto, C tipo, F preço atual, H preço promoção, I início, J fim, L status)
  shopee.json  'Regra Especial Shopee AGO2026'!A1:K (A produto, I valor de venda)
  anterior.json (opcional) a linha do dia anterior na aba RESUMO DIÁRIO TIKTOK: {"shopee":[b,i,c],"ml":[b,i,c]}
Saída: canais.json (percentuais e contagens) e canais_resumo.txt
Preço do TikTok = preço na PROMOÇÕES (o que o cliente vê); se o SKU não está lá, o do CONTROLE.
"Mesmo preço" = diferença de até 1%. Produtos casados pelo nome (as abas do comercial não têm SKU).
"""
import datetime
import difflib
import json
import os
import re
import sys
import unicodedata

TOL = 0.01


def num(s):
    s = str(s or '').replace('R$', '').replace('%', '').replace(' ', '').replace(' ', '')
    if not s:
        return None
    if ',' in s:
        s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def norm(nome):
    t = unicodedata.normalize('NFKD', str(nome)).encode('ascii', 'ignore').decode().lower()
    t = re.split(r'\s(?:cor|tamanho|tamanho do quadro)\s*:', t)[0]
    t = t.split(';')[0]
    t = re.sub(r'[^a-z0-9]+', ' ', t).strip()
    return t


def data(s):
    try:
        return datetime.datetime.strptime(str(s).strip(), '%d/%m/%Y').date()
    except ValueError:
        return None


def main():
    w, hoje_s = sys.argv[1], sys.argv[2]
    ant = json.load(open(sys.argv[3])) if len(sys.argv) > 3 and os.path.exists(sys.argv[3]) else None
    hoje = data(hoje_s)
    g = lambda r, i: r[i] if len(r) > i else ''
    ctl = json.load(open(os.path.join(w, 'ctl.json')))['values']
    ml = json.load(open(os.path.join(w, 'ml.json')))['values']
    sh = json.load(open(os.path.join(w, 'shopee.json')))['values']

    # ML: por produto, preço vigente (promoção ativa no prazo, senão preço atual); prefere Clássico, depois o menor
    mlp = {}
    for r in ml[1:]:
        nome = norm(g(r, 1))
        if not nome:
            continue
        atual, promo = num(g(r, 5)), num(g(r, 7))
        ini, fim = data(g(r, 8)), data(g(r, 9))
        ativa = g(r, 11).strip().lower() == 'ativa' and promo and (not ini or ini <= hoje) and (not fim or hoje <= fim)
        p = promo if ativa else atual
        if not p:
            continue
        cand = (0 if g(r, 2).strip().lower().startswith('cl') else 1, p, bool(ativa), ini)
        if nome not in mlp or cand < mlp[nome]:
            mlp[nome] = cand
    shp = {}
    for r in sh[1:]:
        nome, p = norm(g(r, 0)), num(g(r, 8))
        if nome and p and nome not in shp:
            shp[nome] = p

    def acha(nome, base):
        if nome in base:
            return base[nome]
        m = difflib.get_close_matches(nome, base.keys(), n=1, cutoff=0.93)
        return base[m[0]] if m else None

    res = {'shopee': [0, 0, 0], 'ml': [0, 0, 0]}
    motivo = {'ml_promo': 0, 'piso10': 0, 'outros': 0}
    total, vistos = 0, set()
    for r in ctl[1:]:
        sku, nome = g(r, 2).strip(), g(r, 1)
        if not sku or sku in vistos:
            continue
        tt = num(g(r, 30)) or num(g(r, 11))
        if not tt:
            continue
        vistos.add(sku)
        total += 1
        mg = num(g(r, 12))
        n = norm(nome)
        for canal, base in (('shopee', shp), ('ml', mlp)):
            v = acha(n, base)
            if v is None:
                continue
            p = v[1] if canal == 'ml' else v
            if tt < p * (1 - TOL):
                res[canal][0] += 1
            elif tt > p * (1 + TOL):
                res[canal][2] += 1
                if canal == 'ml' and v[2]:
                    motivo['ml_promo'] += 1
                elif mg is not None and mg < 12:
                    motivo['piso10'] += 1
                else:
                    motivo['outros'] += 1
            else:
                res[canal][1] += 1

    def pct(a):
        t = sum(a)
        return [round(100 * x / t, 1) if t else 0 for x in a], t

    out = {'data': hoje_s, 'skus_tiktok': total}
    linhas = ['Comparação de preço (TikTok x outros canais; "mesmo preço" = até 1% de diferença):']
    for canal, rot in (('shopee', 'Shopee'), ('ml', 'Mercado Livre')):
        p, t = pct(res[canal])
        out[canal] = p
        out[canal + '_n'] = t
        txt = (f'- {rot}: {p[0]:.1f}% mais barato no TikTok | {p[1]:.1f}% mesmo preço | {p[2]:.1f}% mais caro '
               f'({t} de {total} produtos comparados)')
        if ant and ant.get(canal):
            d = [round(p[i] - ant[canal][i], 1) for i in range(3)]
            if max(abs(x) for x in d) < 2:
                txt += ' – praticamente igual a ontem.'
            else:
                txt += f' – variação desde ontem: mais barato {d[0]:+.1f} p.p., mesmo preço {d[1]:+.1f} p.p., mais caro {d[2]:+.1f} p.p.'
        linhas.append(txt)
    out['motivo_ml_caro'] = motivo
    linhas.append('Por quê: o preço do TikTok nasce do menor preço entre Shopee e ML (regra do CONTROLE), por isso a maioria '
                  'fica igual ou abaixo. Ficamos mais caros quando: (1) entra uma promoção no ML depois que o preço do TikTok '
                  f'foi definido ({motivo["ml_promo"]} produtos hoje); (2) o preço foi subido para manter a margem mínima de 10%, '
                  f'porque a taxa do TikTok (6% + R$ 6 + frete 6%) pesa mais em alguns itens ({motivo["piso10"]}); '
                  f'(3) preço da Shopee/ML mudou depois (comercial reprecificou) ou ajuste manual ({motivo["outros"]}). Contagens somam os dois canais.')
    json.dump(out, open(os.path.join(w, 'canais.json'), 'w'))
    open(os.path.join(w, 'canais_resumo.txt'), 'w', encoding='utf-8').write('\n'.join(linhas) + '\n')
    print('\n'.join(linhas))


if __name__ == '__main__':
    main()
