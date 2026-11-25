---
name: tiktok-custo-diario
description: Rotina diária (agendada por volta de 1h50, horário de Brasília) que confere no Bling o custo de todos os SKUs do CONTROLE ANÚNCIOS TIKTOKSHOP, grava os custos que mudaram (col. E; anterior na col. AC), registra na aba HISTÓRICO CUSTO TIKTOK e manda por e-mail a lista de produtos que precisam de reajuste (custo subiu e margem < 10%). Use quando a tarefa agendada disparar ou quando o usuário pedir "atualiza o custo", "roda a rotina de custo" ou /tiktok-custo-diario.
---

# Atualização diária de custo (Bling → CONTROLE) com alerta por e-mail

Roda sem ninguém olhando: **não faça perguntas**. Só leitura no Bling (nunca crie nem altere nada lá).
**Nunca mexa em preço** (col. L do CONTROLE nem aba PROMOÇÕES): a rotina só atualiza custo e avisa.

- Planilha `1ZpeObRddsYOU6lphQaRuH2j4O_dgEzCUdV4ODTxst9w` (pt-BR: fórmulas com `;`).
- CONTROLE sheetId `236203424` (tem filtro do usuário na col. B: não mexa; `updateCells` grava nas linhas ocultas).
- HISTÓRICO CUSTO TIKTOK sheetId `2026112501`: B2 = última execução, D2 = situação; cabeçalho na linha 4; dados a partir da linha 5.
- E-mail: `lbandeira2029@gmail.com` (to) e `lbandeira2029.cursos@gmail.com` (cc), pelo Gmail (`mcp__Gmail__send_message`).
- Pasta de trabalho `$W`: crie uma pasta nova no scratchpad (ex.: `$SCRATCH/custo_AAAAMMDD`). Scripts com `python3 -I`.
- Data/hora: `TZ=America/Sao_Paulo date '+%d/%m/%Y %H:%M'`.

## 0. Ciclo de reforço
A tarefa dispara duas vezes por noite (≈1h50 e ≈4h50). Leia `'HISTÓRICO CUSTO TIKTOK'!B2:D2`.
Se B2 já tem a data de hoje e D2 começa com "OK", **pare** sem mandar e-mail (a 1ª rodada já resolveu).
Se começa com "INCOMPLETA" ou é de outro dia, rode tudo.

## 1. Bling (custo do cadastro = custo do fornecedor padrão; conferido em 24/11/2026 em 1.003 de 1.003 SKUs)
1. Carregue `mcp__BLING__listProducts`. Lista de códigos: `dados/mapa.json` → `codigos_consulta` (≈1.096). Em lotes de 100:
   - `listProducts(codigos=lote, criterio="5", fields=["codigo","precoCusto"], limite=100)`; se `has_more`, repita com `pagina=2…`.
   - A ferramenta omite os inativos: repita o lote com `criterio="3"` (inativos).
   - No máximo 2 chamadas em paralelo. Erro 429: espere ~60 s (comando em background) e tente de novo, até 3 vezes.
2. Escreva cada produto devolvido em `$W/bling.txt`, uma linha `codigo;precoCusto` (ponto decimal, como vem). Pode ir
   acrescentando com `cat >> $W/bling.txt <<'EOF'` a cada lote.
3. Se a cota diária do Bling acabar ou algum lote falhar 3 vezes: siga com o que tem, e a situação vira "INCOMPLETA".

## 2. Planilha e comparação
1. `get_values 'CONTROLE ANÚNCIOS TIKTOKSHOP 03.10'!A1:AH1281` (vai para arquivo; copie para `$W/ctl.json`).
2. `python3 -I .claude/skills/tiktok-custo-diario/scripts/custo_diario.py $W "<data hora>"`
   Gera `req_custo.json`, `hist.json`, `resumo.txt`, `info.json`. Kits = Σ quantidade × custo dos componentes (mapa.json).
   SKUs com `ignorar` no mapa (sapatilhas MX100 excluídas no Bling, 014055 custo 0) ficam de fora.

## 3. Gravar (só se `info.json` → `mudou` > 0)
1. `update_spreadsheet` com o conteúdo de `req_custo.json` (AC = custo anterior, E = custo novo).
2. `append_values` em `'HISTÓRICO CUSTO TIKTOK'!A5:N` com as linhas de `hist.json` (USER_ENTERED).
3. Sempre (mesmo sem mudança): `update_formulas` em `'HISTÓRICO CUSTO TIKTOK'!B2:D2` =
   `[["<data hora>", "Situação:", "OK – <n> custos alterados, <a> alertas"]]` ou `"INCOMPLETA – <motivo>"`.
   (C2 já tem o texto "Situação:"; reescreva igual.)

## 4. E-mail (sempre, exceto quando o passo 0 parar)
`mcp__Gmail__send_message` para `lbandeira2029@gmail.com` com cc `lbandeira2029.cursos@gmail.com`.
- Assunto: `[TikTok] Custo atualizado – <n> alerta(s) de reajuste – <dd/mm>` (com alertas) ou
  `[TikTok] Custo atualizado – nenhum reajuste necessário – <dd/mm>`; se incompleta, comece com `[TikTok] ATENÇÃO: rotina incompleta`.
- Corpo em `htmlBody`: o texto de `resumo.txt`, com os alertas numa tabela (SKU, produto, linha, custo antes → depois,
  preço/margem CONTROLE, preço/margem PROMOÇÕES, preço mínimo p/ 10%) e o link da planilha:
  https://docs.google.com/spreadsheets/d/1ZpeObRddsYOU6lphQaRuH2j4O_dgEzCUdV4ODTxst9w
  Envie também `body` em texto puro (sem Markdown).
- Se o Gmail falhar, deixe o resumo na mensagem final (vai para o e-mail da conta e para o celular).

## 5. Mensagem final
Termine com o conteúdo de `resumo.txt` (curto). Não faça commit nem push.

## Quando a lista de produtos mudar
`dados/mapa.json` é o mapa SKU → código no Bling (+ composição dos kits). Foi montado em 24/11/2026 com os 1.212 SKUs do
CONTROLE. SKU novo no CONTROLE que não está no mapa é ignorado pela rotina: depois de uma carga de produtos novos
(`/tiktok-novos-produtos`), acrescente-os ao mapa (código Bling, e `kit: [[qtd, codigo], …]` se for kit) e faça commit.
