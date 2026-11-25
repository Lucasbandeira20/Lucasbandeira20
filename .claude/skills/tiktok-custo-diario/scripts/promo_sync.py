"""Leva para a PROMOÇÕES TIKTOK os preços que o usuário mudou à mão no CONTROLE (col. L).

Uso: python3 -I promo_sync.py <pasta> "<dd/mm/aaaa hh:mm>"
Entrada: <pasta>/ctl.json (CONTROLE A1:AH1281) e <pasta>/promo.json (PROMOÇÕES A1:P3000)
Saída:
  promo_req.json    requests do batchUpdate (PROMOÇÕES: C texto com ponto, K preço, L desconto, P data da alteração)
  promo_upload.json [[product_id, sku_id, "preço"]] das linhas alteradas (para o Excel FixedPriceWithSKU)
  promo_resumo.txt  texto para o e-mail
"""
import json
import os
import sys

SHEET_PROMO = 293760526


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


def brl(v):
    return 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def main():
    w, quando = sys.argv[1], sys.argv[2]
    g = lambda r, i: r[i] if len(r) > i else ''
    ctl = json.load(open(os.path.join(w, 'ctl.json')))['values']
    promo = json.load(open(os.path.join(w, 'promo.json')))['values']
    preco = {}
    for r in ctl[1:]:
        sku = g(r, 2).strip()
        L, N = num(g(r, 11)), num(g(r, 13))
        if sku and L:
            preco.setdefault(sku, (L, N, g(r, 1)))
    req, upload, mudou, barrado = [], [], [], []
    for i, r in enumerate(promo[1:], start=2):
        sku = g(r, 8).strip()
        atual = num(str(g(r, 2)).replace('.', ',')) if g(r, 2) else None
        if not sku or sku not in preco or atual is None:
            continue
        L, N, nome = preco[sku]
        if abs(L - atual) < 0.005:
            continue
        cheio = num(g(r, 9)) or N
        if cheio and L >= cheio - 0.005:
            barrado.append((sku, nome, atual, L, cheio))
            continue
        vals = [{'userEnteredValue': {'stringValue': f'{L:.2f}'}}]
        req.append({'updateCells': {'start': {'sheetId': SHEET_PROMO, 'rowIndex': i - 1, 'columnIndex': 2},
                                    'rows': [{'values': vals}], 'fields': 'userEnteredValue'}})
        cols = [{'userEnteredValue': {'numberValue': L}},
                {'userEnteredValue': {'numberValue': round((cheio or L) - L, 2)}}]
        req.append({'updateCells': {'start': {'sheetId': SHEET_PROMO, 'rowIndex': i - 1, 'columnIndex': 10},
                                    'rows': [{'values': cols}], 'fields': 'userEnteredValue'}})
        req.append({'updateCells': {'start': {'sheetId': SHEET_PROMO, 'rowIndex': i - 1, 'columnIndex': 15},
                                    'rows': [{'values': [{'userEnteredValue': {'stringValue': f'{quando} (era {atual:.2f})'}}]}],
                                    'fields': 'userEnteredValue'}})
        upload.append([g(r, 0).strip(), g(r, 1).strip(), f'{L:.2f}'])
        mudou.append((sku, nome, atual, L, i))
    json.dump(req, open(os.path.join(w, 'promo_req.json'), 'w'), separators=(',', ':'))
    json.dump(upload, open(os.path.join(w, 'promo_upload.json'), 'w'))
    t = []
    if mudou:
        skus = sorted({m[0] for m in mudou})
        t.append(f'PROMOÇÕES atualizada: {len(mudou)} linha(s), {len(skus)} SKU(s) com preço novo do CONTROLE. '
                 'Excel de upload (FixedPriceWithSKU) em anexo: suba no painel do TikTok para o preço valer lá.')
        vistos = set()
        for sku, nome, a, L, _ in mudou:
            if sku in vistos:
                continue
            vistos.add(sku)
            t.append(f'- SKU {sku} | {nome[:60]} | {brl(a)} -> {brl(L)}')
    else:
        t.append('PROMOÇÕES: nenhum preço novo no CONTROLE.')
    if barrado:
        t.append(f'Não atualizados ({len(barrado)}): preço do CONTROLE igual ou acima do preço cheio (o TikTok recusa a oferta):')
        for sku, nome, a, L, c in barrado:
            t.append(f'- SKU {sku} | {nome[:60]} | CONTROLE {brl(L)} x cheio {brl(c)} (promoção segue {brl(a)})')
    open(os.path.join(w, 'promo_resumo.txt'), 'w', encoding='utf-8').write('\n'.join(t) + '\n')
    print('\n'.join(t))


if __name__ == '__main__':
    main()
