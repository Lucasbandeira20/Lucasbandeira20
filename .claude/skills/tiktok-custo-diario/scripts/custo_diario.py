"""Compara o custo do Bling com a col. E do CONTROLE e prepara as gravações e o alerta.

Uso: python3 -I custo_diario.py <pasta_trabalho> <data dd/mm/aaaa hh:mm>

Entrada na pasta de trabalho:
  bling.txt  linhas "codigo;precoCusto" (uma por produto devolvido pelo listProducts)
  ctl.json   get_values de 'CONTROLE ANÚNCIOS TIKTOKSHOP 03.10'!A1:AH1281 ({range, values})
Saída na mesma pasta:
  req_custo.json   requests do batchUpdate (col. E = custo novo, col. AC = custo anterior)
  hist.json        linhas para a aba HISTÓRICO CUSTO TIKTOK (A:N), uma por SKU que mudou
  resumo.txt       texto do alerta (vai no e-mail e na mensagem final)
  info.json        contagens
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SHEET_CTL = 236203424


def num(s):
    s = str(s or '').replace('R$', '').replace(' ', '').replace(' ', '')
    if not s:
        return None
    if ',' in s:
        s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def margem(custo, preco):
    if not preco or custo is None:
        return None
    taxa = preco * 0.1 + 4 if preco < 50 else preco * 0.06 + 6
    return 1 - (custo + taxa + preco * 0.073 + min(preco * 0.06, 50)) / preco


def preco_minimo(custo, alvo=0.10):
    """Primeiro preço redondo (regra do CLAUDE.md) com margem >= alvo."""
    cands = [x + 0.90 for x in range(1, 50)]
    for dez in range(50, 100000, 10):
        for d in (5.10, 4.50, 2.10, 1.10, 0.10, 0.01):
            p = round(dez - d, 2)
            if p >= 50:
                cands.append(p)
        if len(cands) > 6000:
            break
    for p in sorted(set(round(c, 2) for c in cands)):
        m = margem(custo, p)
        if m is not None and m >= alvo:
            return p
    return None


def brl(v):
    return 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def pct(v):
    return '—' if v is None else f'{v * 100:.1f}%'.replace('.', ',')


def main():
    w, quando = sys.argv[1], sys.argv[2]
    dados = json.load(open(os.path.join(AQUI, '..', 'dados', 'mapa.json')))
    mapa = dados['mapa']

    bling = {}
    for ln in open(os.path.join(w, 'bling.txt'), encoding='utf-8'):
        p = ln.strip().split(';')
        if len(p) >= 2 and p[0]:
            v = num(p[1].replace('.', ',')) if '.' in p[1] and ',' not in p[1] else num(p[1])
            bling[p[0]] = v
            bling.setdefault(p[0].lstrip('0'), v)

    def custo_cod(c):
        return bling.get(c, bling.get(c.lstrip('0')))

    ctl = json.load(open(os.path.join(w, 'ctl.json')))['values']
    g = lambda r, i: r[i] if len(r) > i else ''

    mudou, faltou, alertas = [], [], []
    for i, r in enumerate(ctl[1:], start=2):
        sku = g(r, 2).strip()
        if not sku or sku not in mapa:
            continue
        e = mapa[sku]
        if 'ignorar' in e:
            continue
        if 'kit' in e:
            partes = [(q, custo_cod(c)) for q, c in e['kit']]
            if any(c is None for _, c in partes):
                faltou.append(sku)
                continue
            novo = round(sum(q * c for q, c in partes), 2)
        else:
            novo = custo_cod(e['codigo_bling'])
            if novo is None:
                faltou.append(sku)
                continue
            novo = round(novo, 2)
        if not novo:
            continue  # custo 0 no Bling: não sobrescreve
        velho = num(g(r, 4))
        if velho is not None and abs(novo - velho) < 0.015:  # ignora arredondamento de 1 centavo
            continue
        L = num(g(r, 11))
        promo = num(g(r, 30))
        mL, mP = margem(novo, L), margem(novo, promo)
        subiu = velho is not None and novo > velho
        alerta = subiu and ((mL is not None and mL < 0.10) or (mP is not None and mP < 0.10))
        pmin = preco_minimo(novo) if alerta else None
        x = dict(linha=i, sku=sku, nome=g(r, 1), velho=velho, novo=novo, L=L, mL=mL, promo=promo, mP=mP,
                 alerta=alerta, pmin=pmin, lote=g(r, 33))
        mudou.append(x)
        if alerta:
            alertas.append(x)

    # requests: blocos contíguos para E (col 4) e AC (col 28)
    req, bloco = [], []
    def fecha(b):
        if not b:
            return
        for col, k in ((28, 'velho'), (4, 'novo')):
            req.append({'updateCells': {
                'start': {'sheetId': SHEET_CTL, 'rowIndex': b[0]['linha'] - 1, 'columnIndex': col},
                'rows': [{'values': [{'userEnteredValue': {'numberValue': x[k] if x[k] is not None else 0}}]} for x in b],
                'fields': 'userEnteredValue'}})
    for x in mudou:
        if bloco and x['linha'] != bloco[-1]['linha'] + 1:
            fecha(bloco)
            bloco = []
        bloco.append(x)
    fecha(bloco)
    json.dump(req, open(os.path.join(w, 'req_custo.json'), 'w'), separators=(',', ':'))

    hist = [[quando, "'" + x['sku'], x['nome'], x['linha'], x['velho'], x['novo'],
             round(x['novo'] - (x['velho'] or 0), 2), x['L'] or '',
             round(x['mL'] * 100, 1) if x['mL'] is not None else '', x['promo'] or '',
             round(x['mP'] * 100, 1) if x['mP'] is not None else '',
             'SIM' if x['alerta'] else '', x['pmin'] or '', x['lote']] for x in mudou]
    json.dump(hist, open(os.path.join(w, 'hist.json'), 'w'), ensure_ascii=False)

    sub = sum(1 for x in mudou if x['velho'] is not None and x['novo'] > x['velho'])
    linhas = [f'Atualização de custo TikTok ({quando})', '']
    if not mudou:
        linhas.append('Nenhum custo mudou no Bling. Nada a reajustar.')
    else:
        linhas.append(f'{len(mudou)} SKUs com custo novo no Bling ({sub} subiram, {len(mudou) - sub} caíram). '
                      'Coluna E do CONTROLE atualizada; custo anterior na coluna AC.')
    linhas.append('')
    if alertas:
        linhas.append(f'ATENÇÃO: {len(alertas)} produto(s) precisam de reajuste de preço (custo subiu e margem < 10%):')
        for x in alertas:
            linhas.append(f"- SKU {x['sku']} | {x['nome'][:60]} | linha {x['linha']} | custo {brl(x['velho'])} -> {brl(x['novo'])} | "
                          f"CONTROLE {brl(x['L']) if x['L'] else '—'} ({pct(x['mL'])}) | "
                          f"PROMOÇÕES {brl(x['promo']) if x['promo'] else '—'} ({pct(x['mP'])}) | "
                          f"preço mínimo p/ 10%: {brl(x['pmin']) if x['pmin'] else '—'}")
    else:
        linhas.append('Nenhum produto ficou abaixo de 10% de margem.')
    if faltou:
        linhas.append('')
        linhas.append(f'{len(faltou)} SKU(s) não voltaram na consulta do Bling (custo mantido): ' + ', '.join(faltou[:40]))
    open(os.path.join(w, 'resumo.txt'), 'w', encoding='utf-8').write('\n'.join(linhas) + '\n')
    json.dump({'mudou': len(mudou), 'subiu': sub, 'alertas': len(alertas), 'faltou': len(faltou),
               'consultados': len(bling)}, open(os.path.join(w, 'info.json'), 'w'))
    print('\n'.join(linhas))


if __name__ == '__main__':
    main()
