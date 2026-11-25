"""Gera o Excel de upload da promoção (modelo FixedPriceWithSKU, colunas A a E) com as linhas alteradas.

Uso: python3 -I promo_excel.py <pasta> <saida.xlsx>   (lê <pasta>/promo_upload.json)
"""
import json
import os
import shutil
import sys

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(AQUI, '..', '..', 'tiktok-novos-produtos', 'assets', 'modelo_promocao_FixedPriceWithSKU.xlsx')

w, out = sys.argv[1], sys.argv[2]
v = json.load(open(os.path.join(w, 'promo_upload.json')))
erros = [r for r in v if len(r[0]) != 19 or len(r[1]) != 19 or ',' in r[2]]
if erros:
    sys.exit(f'IDs fora de 19 dígitos ou preço com vírgula: {erros[:5]}')
shutil.copy(TPL, out)
wb = openpyxl.load_workbook(out)
ws = wb.active
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    for c in row:
        c.value = None
for row in ws.iter_rows(min_row=1, max_row=1):
    for c in row[5:]:
        c.value = None
for i, r in enumerate(v, start=2):
    for j, val in enumerate(r[:3], start=1):
        c = ws.cell(i, j)
        c.value = str(val)
        c.number_format = '@'
wb.save(out)
print(f'{out}: {len(v)} SKUs')
