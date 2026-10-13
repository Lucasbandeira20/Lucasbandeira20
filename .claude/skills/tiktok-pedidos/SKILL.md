---
name: tiktok-pedidos
description: Processa um relatório de pedidos do TikTok Seller Center (arquivo Todos_pedido-AAAA-MM-DD-HH_MM.xlsx, aba OrderSKUList) da Avelar Shop. Compara com a aba ANÁLISE MARGEM VENDAS TIKTOK, adiciona só os pedidos novos (enviados, a enviar e concluídos), atualiza o status dos antigos e marca cancelados e devolvidos. Não mexe na CONCILIAÇÃO FINANCEIRA TIKTOK, que só recebe os demonstrativos financeiros (income/onhold). Use sempre que o usuário enviar a planilha de pedidos, disser "planilha de pedidos", "novos pedidos do TikTok", "todos os pedidos" ou pedir /tiktok-pedidos. O arquivo pode ser do mês completo ou parcial.
---

# Pedidos TikTok Shop → ANÁLISE MARGEM VENDAS

Regras, colunas e histórico estão no `CLAUDE.md` da raiz e na aba **REGRAS E PROCESSO TIKTOK**. Este arquivo é o roteiro.

- Planilha `1ZpeObRddsYOU6lphQaRuH2j4O_dgEzCUdV4ODTxst9w` (pt-BR: fórmulas com `;`).
- sheetIds: ANÁLISE `1935682352`, REGRAS `738877884`.
- Nunca altere o CONTROLE, a PROMOÇÕES nem abas de ML/Shopee.
- **Nunca grave na CONCILIAÇÃO FINANCEIRA TIKTOK com este relatório.** Ele é só de vendas. A CONCILIAÇÃO só é preenchida quando o usuário mandar os demonstrativos financeiros (income por pedido, income resumo, onhold). Pedido cancelado/devolvido também não muda nada lá: a conciliação muda quando o financeiro mostrar.
- O relatório de pedidos **não traz taxas**. Comissão, SFP 6% e taxa por item dos pedidos novos ficam como **fórmula pela regra** (colunas N, O, P). Afiliado e GMV Max só aparecem no income/onhold: quando o usuário mandar esses relatórios, troque N:R pelos valores reais e a coluna D pela situação financeira.
- O relatório tem CPF, endereço e telefone: **nunca copie esses campos** para a planilha.
- Pasta do lote: `$L = $SCRATCH/pedidos_AAAAMMDD`. Copie o .xlsx para lá. Scripts com `python3 -I`.
- Mantenha o usuário informado com frases curtas entre as etapas.

## Passo 1: ler o que já está na planilha
1. `get_values` de `'ANÁLISE MARGEM VENDAS TIKTOK'!A1:D3000`.
2. Salve com o script da outra skill (o range devolvido é cortado no tamanho da aba, ex.: `A1:D1000`; use o range que aparecer no resultado):
   `python3 -I .claude/skills/tiktok-novos-produtos/scripts/salvar_resultado.py "ANÁLISE MARGEM VENDAS TIKTOK'!A1:D1000" $L/analise_AD.json`
3. Confira se a aba tem linhas suficientes (hoje 1000). Se não, `appendDimension` antes de gravar.

## Passo 2: comparar
`python3 -I .claude/skills/tiktok-pedidos/scripts/pedidos.py $L/<arquivo>.xlsx $L/analise_AD.json $L`

Gera `resumo.txt`, `info.json` (linhas de início/fim), `analise_novos_NN.json`, `analise_status_C.json` e `mudancas.json`. Mostre o resumo ao usuário. Se não houver novos nem mudanças, pare.
Novos = status Enviado, A ser enviado ou Concluído, sem cancelamento/devolução, que não estão na coluna B da ANÁLISE.
Pedidos antigos que não vierem no arquivo (relatório parcial) ficam como estão.

## Passo 3: gravar na ANÁLISE
1. `update_formulas` de cada `analise_novos_NN.json` a partir de `A<analise_inicio>` (top-left só; 40 linhas por parte).
   A 1ª linha nova leva todas as fórmulas; as outras vêm com `null` nas colunas de fórmula.
2. Um `update_spreadsheet` com:
   - `copyPaste PASTE_FORMAT` da última linha antiga (A:AD) para as novas;
   - `copyPaste PASTE_FORMULA` da 1ª linha nova para as demais nas colunas H, K, N:P e S:AE (índices 7, 10, 13–15, 18–30).
3. Status: `update_formulas` de `analise_status_C.json` em `C2` (atualiza "Enviado / Entregue" etc. das linhas antigas).
4. Para cada item de `mudancas.json` (cancelado ou devolvido):
   - ANÁLISE, linha `linha_analise`: `D:R` = `[situacao, null, null, 0, null, 0, 0, null, 0, 0, 0, 0, 0, 0, 0]`
     (D situação, G qtd 0, I/J/L:R zerados; H e K continuam fórmula) e `AD` com o motivo (data, quem cancelou, valor reembolsado).
   - Na CONCILIAÇÃO não muda nada. A linha "Diferença (tem que ser zero)" vai mostrar a diferença desses pedidos até chegar o financeiro: avise o usuário.

## Passo 4: conferir
- ANÁLISE: leia `W<ini>:AE<fim>` (o resultado é grande: vem salvo em arquivo; resuma com python). Nenhum `#N/A`/`#REF!`;
  coluna Y (linha no CONTROLE) preenchida. SKU sem linha no CONTROLE aparece em AD como "SKU não está no CONTROLE": avise.
- Resuma ao usuário: quantos novos, margem estimada, quantos abaixo de 10% e por quê (coluna AD), cancelados/devolvidos.

## Passo 5: registrar
- HISTÓRICO da aba REGRAS E PROCESSO TIKTOK (inserir linha logo após o último item de data do HISTÓRICO) e `CLAUDE.md`.
- Commit e push na branch de trabalho.
