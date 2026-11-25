"""Produtos que chegaram (aba Produtos Novos da planilha do comercial, só leitura) e ainda não estão no TikTok.

Uso: python3 -I novos.py <pasta> "<dd/mm/aaaa>" ["<dd/mm/aaaa da última rotina>"]
Entrada:
  pn.json   'Produtos Novos'!A1:J (A data, B tipo, C SKU, D produto, E custo, G site, H shopee, I promo ML)
  ctl.json  CONTROLE A1:AH1281 (C = SKU)
  produtos TikTok: o mais recente ../../tiktok-relatorios-navegador/entrada/produtos_*.csv, se existir
Considera só entradas desde 06/10/2026 (início do TikTok) e ignora Devolução e Balanço.
Saída: novos.json (lista pendente) e novos_resumo.txt
"""
import csv
import datetime
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canais import norm  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
INICIO = datetime.date(2026, 10, 6)


def data(s):
    try:
        return datetime.datetime.strptime(str(s).strip(), '%d/%m/%Y').date()
    except ValueError:
        return None


def chave(s):
    return str(s).strip().lstrip('0').upper()


def main():
    w = sys.argv[1]
    ultima = data(sys.argv[3]) if len(sys.argv) > 3 else None
    g = lambda r, i: r[i] if len(r) > i else ''
    pn = json.load(open(os.path.join(w, 'pn.json')))['values']
    ctl = json.load(open(os.path.join(w, 'ctl.json')))['values']
    no_tt = {chave(g(r, 2)) for r in ctl[1:] if g(r, 2).strip()}
    nomes_tt = {norm(g(r, 1)) for r in ctl[1:] if g(r, 1).strip()}
    arqs = sorted(glob.glob(os.path.join(AQUI, '..', '..', 'tiktok-relatorios-navegador', 'entrada', 'produtos_*.csv')))
    fonte = 'CONTROLE'
    if arqs:
        for r in csv.DictReader(open(arqs[-1], encoding='utf-8')):
            no_tt.add(chave(r['seller_sku']))
            nomes_tt.add(norm(r['product_name']))
        fonte = f'CONTROLE + relatório de produtos do TikTok ({os.path.basename(arqs[-1])[9:22]})'
    pend = {}
    for r in pn[1:]:
        d, tipo, sku = data(g(r, 0)), g(r, 1), g(r, 2).strip()
        if not d or d < INICIO or not sku:
            continue
        if 'devolu' in tipo.lower() or 'balan' in tipo.lower():
            continue
        if chave(sku) in no_tt or norm(g(r, 3)) in nomes_tt:
            continue
        pend[chave(sku)] = {'data': g(r, 0), 'tipo': tipo.strip(), 'sku': sku, 'produto': g(r, 3).strip(),
                            'custo': g(r, 4).strip(), 'shopee': g(r, 7).strip(), 'site': g(r, 6).strip()}
    lista = sorted(pend.values(), key=lambda x: (data(x['data']), x['sku']), reverse=True)
    novos_hoje = [x for x in lista if ultima and data(x['data']) and data(x['data']) >= ultima]
    json.dump(lista, open(os.path.join(w, 'novos.json'), 'w'), ensure_ascii=False)
    t = [f'Produtos que chegaram e ainda não estão no TikTok: {len(lista)} SKU(s) pendentes desde 06/10/2026 '
         f'(sem Devolução e Balanço; conferido contra {fonte}).']
    mostrar = novos_hoje if ultima else lista
    if ultima:
        t.append(f'Entraram desde a última rotina ({ultima:%d/%m}): {len(novos_hoje)}.')
    for x in mostrar[:60]:
        t.append(f"- {x['data']} | SKU {x['sku']} | {x['produto'][:70]} | custo {x['custo']} | {x['tipo']}")
    if len(mostrar) > 60:
        t.append(f'... e mais {len(mostrar) - 60} (lista completa na aba PRODUTOS NOVOS FORA DO TIKTOK).')
    open(os.path.join(w, 'novos_resumo.txt'), 'w', encoding='utf-8').write('\n'.join(t) + '\n')
    print('\n'.join(t[:8]))


if __name__ == '__main__':
    main()
