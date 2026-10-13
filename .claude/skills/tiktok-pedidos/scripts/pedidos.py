"""Compara um relatório de pedidos do TikTok (Todos_pedido / OrderSKUList .xlsx) com a aba
ANÁLISE MARGEM VENDAS TIKTOK e gera os payloads de gravação.

O relatório de pedidos é só de VENDAS: ele alimenta apenas a ANÁLISE. A CONCILIAÇÃO FINANCEIRA
só é preenchida com os demonstrativos financeiros (income / onhold), nunca por este script.

Uso: python3 -I pedidos.py <pedidos.xlsx> <analise_AD.json> <pasta_saida>

- analise_AD.json = get_values de 'ANÁLISE MARGEM VENDAS TIKTOK'!A1:D3000 (salvo com salvar_resultado.py)

Saídas na pasta:
- resumo.txt
- analise_novos_NN.json   linhas novas da ANÁLISE (A:AD), em partes de 40; fórmulas só na 1ª linha nova
- analise_status_C.json   coluna C (status) atualizada para todas as linhas antigas (C2:C<última>)
- mudancas.json           pedidos antigos que viraram cancelado/devolvido (linha na ANÁLISE)
- info.json               linhas de início, quantidades e intervalos de cópia de fórmulas
O relatório pode ser do mês completo ou parcial: pedidos que não vierem no arquivo continuam como estão.
"""
import datetime
import json
import os
import sys

import openpyxl

VALIDOS = ('Enviado', 'A ser enviado', 'Concluído')
CT = "'CONTROLE ANÚNCIOS TIKTOKSHOP 03.10'"
AN = "'ANÁLISE MARGEM VENDAS TIKTOK'"
GMV = "'GMV MAX TIKTOK'"
CAMP = "'CAMPANHAS TIKTOK'"


def brl(s):
    if s in (None, ''):
        return 0.0
    if isinstance(s, (int, float)):
        return float(s)
    return float(str(s).replace('BRL', '').strip().replace('.', '').replace(',', '.') or 0)


def dt(s):
    return datetime.datetime.strptime(s, '%m/%d/%Y %I:%M:%S %p') if s else None


def load(p):
    d = json.load(open(p))
    return d.get('values', []) if isinstance(d, dict) else d


def formulas_analise(r):
    return {
        7: f'=IF(Y{r}="";"";INDEX({CT}!$E$1:$E$1281;Y{r}))',
        10: f'=I{r}-J{r}',
        13: f'=IF(G{r}=0;0;IF(K{r}/G{r}<50;K{r}*0,1;K{r}*0,06))',
        14: f'=MIN(K{r}*0,06;50*G{r})',
        15: f'=IF(G{r}=0;0;IF(K{r}/G{r}<50;4;6)*G{r})',
        18: f'=K{r}*0,073',
        19: f'=H{r}*G{r}',
        20: f'=SUM(N{r}:T{r})',
        21: f'=K{r}-SUM(N{r}:R{r})',
        22: f'=IFERROR(1-U{r}/K{r};"")',
        23: f'=K{r}-U{r}',
        24: f'=IFERROR(MATCH(VALUE(F{r});ARRAYFORMULA(IFERROR(VALUE({CT}!$C$1:$C$1281)));0);"")',
        25: f'=IF(Y{r}="";"";INDEX({CT}!$L$1:$L$1281;Y{r}))',
        26: f'=IF(Y{r}="";"";INDEX({CT}!$M$1:$M$1281;Y{r}))',
        27: f'=IFERROR(W{r}-AA{r};"")',
        28: f'=IF(AB{r}="";"";IF(ABS(AB{r})<=0,005;"OK - conforme CONTROLE";IF(AB{r}>0;"ACIMA DO CONTROLE";"ABAIXO DO CONTROLE")))',
        29: (f'=IF(Y{r}="";"SKU não está no CONTROLE";LET(vu;K{r}/G{r};d;vu-Z{r};'
             f'c;IFERROR(MATCH(F{r};{CAMP}!$E$6:$E$200;0);0);'
             f'p;IF(ABS(d)<0,005;"Preço igual ao CONTROLE";IF(ABS(d+0,5)<0,005;"Vendido a R$ "&TEXT(vu;"#,##0.00")&": preço de campanha do TikTok (CONTROLE − R$ 0,50)";'
             f'IF(ABS(vu-ROUNDDOWN(Z{r}*0,95;2))<0,02;"Vendido a R$ "&TEXT(vu;"#,##0.00")&": 5% abaixo do CONTROLE (R$ "&TEXT(Z{r};"#,##0.00")&"), desconto de campanha/promoção";'
             f'IF(AND(c>0;ABS(vu-IFERROR(INDEX({CAMP}!$K$6:$K$200;c);0))<0,6);'
             f'"Preço da campanha 10.10 (R$ "&TEXT(vu;"#,##0.00")&")";"Vendido a R$ "&TEXT(vu;"#,##0.00")&", "&IF(d<0;"abaixo";"acima")&" do CONTROLE (R$ "&TEXT(Z{r};"#,##0.00")&")"))));'
             f'IF(AND(ISNUMBER(W{r});W{r}<0,1);"MARGEM ABAIXO DE 10%. ";"")&p&". Taxas estimadas pela regra (afiliado e GMV Max só aparecem no income)"'
             f'&IF(AE{r}="SIM";". Produto no GMV Max: se a venda veio do anúncio, desconta ~5%";"")))'),
        30: f'=IF(COUNTIF({GMV}!$D$7:$D;F{r})>0;"SIM";"")',
    }


def chunks(rows, n=40):
    return [rows[i:i + n] for i in range(0, len(rows), n)]


def main():
    xlsx, an_p, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    ws = openpyxl.load_workbook(xlsx, data_only=True).worksheets[0]
    rows = [r for r in ws.iter_rows(values_only=True) if any(c not in (None, '') for c in r)]
    h = list(rows[0])
    data = [dict(zip(h, r)) for r in rows[1:] if str(r[0]).isdigit()]
    rel = {str(d['Order ID']): d for d in data}

    an = load(an_p)
    an_ids = {str(r[1]).lstrip("'"): i + 1 for i, r in enumerate(an) if i > 0 and len(r) > 1 and r[1]}
    last_an = max(an_ids.values()) if an_ids else 1

    # status atualizado das linhas antigas (coluna C) e mudanças para cancelado/devolvido
    col_c, mudancas = [], []
    for row in range(2, last_an + 1):
        r = an[row - 1] if row - 1 < len(an) else []
        pid = str(r[1]).lstrip("'") if len(r) > 1 else ''
        atual = r[2] if len(r) > 2 else ''
        d = rel.get(pid)
        if not d:
            col_c.append([atual])
            continue
        novo = f"{d['Order Status']} / {d['Order Substatus'] or ''}".strip(' /')
        col_c.append([novo])
        tipo = d.get('Cancelation/Return Type') or ''
        if d['Order Status'] == 'Cancelado' or tipo:
            sit = r[3] if len(r) > 3 else ''
            if sit.startswith(('CANCELADO', 'DEVOLVIDO')):
                continue
            mudancas.append({
                'pedido': pid, 'linha_analise': row,
                'status': d['Order Status'], 'tipo': tipo, 'sku': d['Seller SKU'],
                'reembolso': brl(d.get('Order Refund Amount')), 'qtd_devolvida': d.get('Sku Quantity of return'),
                'cancelado_em': d.get('Cancelled Time'), 'motivo': d.get('Cancel Reason'), 'por': d.get('Cancel By'),
                'situacao': 'CANCELADO' if d['Order Status'] == 'Cancelado' else 'DEVOLVIDO (reembolso)',
            })

    novos = [d for d in data if str(d['Order ID']) not in an_ids and d['Order Status'] in VALIDOS
             and not d.get('Cancelation/Return Type')]
    novos.sort(key=lambda d: dt(d['Created Time']))

    an_rows = []
    r0 = last_an + 1
    for i, d in enumerate(novos):
        q = int(d['Quantity'])
        cheio = brl(d['SKU Subtotal Before Discount'])
        dl = brl(d['SKU Seller Discount'])
        var = d['Variation'] or 'Padrão'
        prod = d['Product Name'] + ('' if var == 'Padrão' else ' - ' + var)
        status = f"{d['Order Status']} / {d['Order Substatus'] or ''}".strip(' /')
        row = [dt(d['Created Time']).strftime('%d/%m/%Y %H:%M'), "'" + str(d['Order ID']), status,
               'ESTIMADO (sem extrato)', prod, "'" + str(d['Seller SKU']), q, None, cheio, dl, None,
               brl(d['SKU Platform Discount']), brl(d['Order Amount']), None, None, None, 0, 0,
               None, None, None, None, None, None, None, None, None, None, None, None, None]
        if i == 0:
            for k, v in formulas_analise(r0).items():
                row[k] = v
        an_rows.append(row)

    for i, ch in enumerate(chunks(an_rows)):
        json.dump(ch, open(f'{out}/analise_novos_{i:02d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    json.dump(mudancas, open(f'{out}/mudancas.json', 'w'), ensure_ascii=False, indent=1)
    info = {'analise_inicio': r0, 'analise_fim': r0 + len(an_rows) - 1, 'novos': len(novos),
            'status_ate_linha': last_an,
            'copiar_formulas_analise_colunas': 'H,K,N,O,P,S:AE (da linha inicial para as demais)'}
    json.dump(info, open(f'{out}/info.json', 'w'), ensure_ascii=False, indent=1)

    from collections import Counter
    st = Counter(d['Order Status'] for d in data)
    datas = sorted(dt(d['Created Time']) for d in data)
    linhas = [f"Relatório: {len(data)} pedidos de {datas[0]:%d/%m/%Y} a {datas[-1]:%d/%m/%Y}. Status: {dict(st)}",
              f"Já na ANÁLISE: {sum(1 for k in rel if k in an_ids)} de {len(an_ids)} (os que não vieram ficam como estão).",
              f"NOVOS para a ANÁLISE: {len(novos)} ({dict(Counter(d['Order Status'] for d in novos))}). "
              f"Linhas {r0} a {r0 + len(novos) - 1}.",
              f"Pedidos antigos que viraram cancelado/devolvido: {len(mudancas)}"]
    for m in mudancas:
        linhas.append(f"  - {m['pedido']} (linha {m['linha_analise']}, SKU {m['sku']}): {m['status']} {m['tipo']}, reembolso R$ {m['reembolso']:.2f}")
    linhas.append(f"SKUs nos novos: {dict(Counter(d['Seller SKU'] for d in novos).most_common(15))}")
    open(f'{out}/resumo.txt', 'w').write('\n'.join(linhas))
    print('\n'.join(linhas))


if __name__ == '__main__':
    main()
