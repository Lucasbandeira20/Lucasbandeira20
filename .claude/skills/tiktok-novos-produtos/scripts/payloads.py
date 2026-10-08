"""Passo 4: monta os arquivos de valores para colar na planilha.

Uso: python3 -I payloads.py <pasta_lote> [linhas_por_parte=80]

Gera em <pasta_lote>/payload/:
- base_partN.json: linhas A..T da BASE (IDs como texto, preço e medidas como número), em partes;
- ctl_BC.json, ctl_E.json, ctl_L.json, ctl_N.json, ctl_T.json, ctl_ZA.json: colunas do CONTROLE
  (Produto+SKU, Custo, Valor de venda, Preço cheio, OBS, Preço ML/Shopee de referência).
"""
import json
import os
import sys

L = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 80
P = f'{L}/payload'
os.makedirs(P, exist_ok=True)

novos = json.load(open(f'{L}/novos.json'))
for k in range(0, len(novos), n):
    json.dump(novos[k:k + n], open(f'{P}/base_part{k // n}.json', 'w'), ensure_ascii=False)
print(f'BASE: {len(novos)} linhas em {(len(novos) + n - 1) // n} parte(s) de até {n}')

if os.path.exists(f'{L}/linhas.json'):
    ls = json.load(open(f'{L}/linhas.json'))
    cols = dict(BC=[[x['nome'], x['sku']] for x in ls], E=[[x['c']] for x in ls], L=[[x['p']] for x in ls],
                N=[[x['cheio']] for x in ls], T=[['; '.join(x['obs'])] for x in ls],
                ZA=[[x['ml'] or '', x['shp'] or ''] for x in ls])
    for k, v in cols.items():
        json.dump(v, open(f'{P}/ctl_{k}.json', 'w'), ensure_ascii=False)
    print(f'CONTROLE: {len(ls)} linhas')
