"""Reduz os relatórios baixados do TikTok ao que as rotinas usam, SEM dados pessoais.

Uso: python3 -I extrair.py <arquivo_pedidos.csv|.xlsx|-> <arquivo_produtos.zip|.xlsx|-> <carimbo AAAAMMDD_HHMM>
Grava em ../entrada/:
  pedidos_<carimbo>.csv   só as colunas usadas pelo /tiktok-pedidos (sem CPF, nome, telefone, endereço)
  produtos_<carimbo>.csv  product_id, sku_id, seller_sku, nome, variação, preço, status
Use "-" para pular um dos arquivos.
"""
import csv
import glob
import io
import os
import sys
import tempfile
import zipfile

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, '..', 'entrada')
COLS_PED = ['Order ID', 'Order Status', 'Order Substatus', 'Cancelation/Return Type', 'Seller SKU', 'Product Name',
            'Variation', 'Quantity', 'Sku Quantity of return', 'SKU Subtotal Before Discount', 'SKU Platform Discount',
            'SKU Seller Discount', 'Order Amount', 'Order Refund Amount', 'Cancel By', 'Cancel Reason',
            'Created Time', 'Cancelled Time']


def ler_pedidos(p):
    if p.lower().endswith('.csv'):
        txt = open(p, encoding='utf-8-sig').read()
        rows = list(csv.reader(io.StringIO(txt)))
        rows = [[c.strip().strip('\t') for c in r] for r in rows if any(c.strip() for c in r)]
    else:
        ws = openpyxl.load_workbook(p, data_only=True, read_only=True).worksheets[0]
        rows = [['' if c is None else str(c).strip() for c in r] for r in ws.iter_rows(values_only=True)]
        rows = [r for r in rows if any(r)]
    h = rows[0]
    idx = [h.index(c) for c in COLS_PED]
    out = [COLS_PED] + [[r[i] if i < len(r) else '' for i in idx] for r in rows[1:] if r and r[0].strip().isdigit()]
    return out


def ler_produtos(p):
    arqs = []
    if p.lower().endswith('.zip'):
        d = tempfile.mkdtemp()
        with zipfile.ZipFile(p) as z:
            z.extractall(d)
        arqs = sorted(glob.glob(os.path.join(d, '**', '*.xlsx'), recursive=True))
    else:
        arqs = [p]
    out = [['product_id', 'sku_id', 'seller_sku', 'product_name', 'variation_value', 'price', 'product_status']]
    for a in arqs:
        ws = openpyxl.load_workbook(a, data_only=True)['Template']  # read_only lê só 5 linhas neste arquivo
        rows = list(ws.iter_rows(values_only=True))
        h = [str(x) for x in rows[0]]
        ix = [h.index(c) for c in out[0]]
        for r in rows[5:]:
            if r and r[0] and str(r[0]).strip().isdigit():
                out.append(['' if r[i] is None else str(r[i]).strip() for i in ix])
    return out


def main():
    ped, prod, carimbo = sys.argv[1:4]
    os.makedirs(SAIDA, exist_ok=True)
    if ped != '-':
        rows = ler_pedidos(ped)
        with open(os.path.join(SAIDA, f'pedidos_{carimbo}.csv'), 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(rows)
        print('pedidos', len(rows) - 1)
    if prod != '-':
        rows = ler_produtos(prod)
        with open(os.path.join(SAIDA, f'produtos_{carimbo}.csv'), 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(rows)
        print('skus', len(rows) - 1)


if __name__ == '__main__':
    main()
