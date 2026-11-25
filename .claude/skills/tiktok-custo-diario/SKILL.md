---
name: tiktok-custo-diario
description: Rotina da madrugada (3h01, reforço 5h01, horário de Brasília) do TikTok Shop da Avelar Shop. Sem navegador: custo no Bling → CONTROLE, preços novos do CONTROLE → PROMOÇÕES (+ Excel de upload), comparação de preço com Shopee e ML, produtos novos que ainda não estão no TikTok, pedidos baixados de dia → ANÁLISE, e um e-mail com tudo. Use quando a tarefa agendada disparar ou o usuário pedir "roda a rotina da madrugada", "atualiza o custo" ou /tiktok-custo-diario.
---

# Rotina da madrugada (sem navegador)

Roda sem ninguém olhando: **não faça perguntas**. Se uma etapa falhar, registre o motivo, siga com as outras e diga no e-mail.

## Regras fixas
- **Planilha nossa** (pode gravar): `1ZpeObRddsYOU6lphQaRuH2j4O_dgEzCUdV4ODTxst9w` (pt-BR: fórmulas com `;`).
  CONTROLE `236203424` (filtro do usuário na col. B: não mexa; use `updateCells`/`update_formulas`), PROMOÇÕES `293760526`,
  HISTÓRICO CUSTO TIKTOK `2026112501`, RESUMO DIÁRIO TIKTOK `2026112502`, PRODUTOS NOVOS FORA DO TIKTOK `2026112503`.
- **Planilha do comercial "Plano de Ação Avelar Shop"** `1EFTCnCdn6-r8DRNOW1CrPfmjxE2luqY_kma2H_uI6J8`:
  **SÓ LEITURA. JAMAIS grave, formate, filtre ou crie nada nela** (outras pessoas trabalham nela). Só `get_values`.
- Bling: só leitura. Nunca mude preço no CONTROLE (col. L); a PROMOÇÕES só copia o preço que o usuário já pôs no CONTROLE.
- E-mail (Gmail `send_message`): to `lbandeira2029@gmail.com`, cc `lbandeira2029.cursos@gmail.com`.
- Pasta de trabalho `$W` nova no scratchpad (ex.: `$SCRATCH/noite_AAAAMMDD`). Scripts em `.claude/skills/tiktok-custo-diario/scripts/`, com `python3 -I`.
- Data/hora: `TZ=America/Sao_Paulo date '+%d/%m/%Y %H:%M'`.

## 0. Ciclo de reforço
Leia `'HISTÓRICO CUSTO TIKTOK'!B2:D2`. Se B2 é de hoje e D2 começa com "OK", pare sem e-mail (a 1ª rodada já resolveu).

## 1. Leituras (salve cada resultado em `$W`)
- `ctl.json` ← `'CONTROLE ANÚNCIOS TIKTOKSHOP 03.10'!A1:AH1281`
- `promo.json` ← `'PROMOÇÕES TIKTOK'!A1:P3000`
- Do comercial (só leitura): `pn.json` ← `'Produtos Novos'!A1:J6000`; `ml.json` ← `'Controle Promoção ML'!A1:N3000`;
  `shopee.json` ← `'Regra Especial Shopee AGO2026'!A1:K3000`
- `anterior.json`: última linha de `'RESUMO DIÁRIO TIKTOK'!A2:N1000` como `{"data":A,"shopee":[B,C,D],"ml":[F,G,H]}`
  (números com ponto; se não houver linha, não crie o arquivo).
Resultados grandes vão para arquivo automaticamente: copie o arquivo para o nome acima.

## 2. Custo (Bling → CONTROLE)
1. `mcp__BLING__listProducts` em lotes de 100 com os códigos de `dados/mapa.json` → `codigos_consulta`:
   `criterio="5"`, `fields=["codigo","precoCusto"]`, `limite=100` (se `has_more`, `pagina=2…`) e repita o lote com `criterio="3"` (inativos).
   No máximo 2 chamadas em paralelo; 429 → espere ~60 s e tente até 3 vezes.
2. Grave cada produto em `$W/bling.txt` (`codigo;precoCusto`, ponto decimal), acrescentando com `cat >> … <<'EOF'`.
3. `custo_diario.py $W "<data hora>"` → `req_custo.json`, `hist.json`, `resumo.txt`, `info.json`.
4. Se `mudou` > 0: `update_spreadsheet` com `req_custo.json`; `append_values` em `'HISTÓRICO CUSTO TIKTOK'!A5:N` com `hist.json`.
   Depois de gravar o custo, **releia** `ctl.json` (a margem e a col. AE mudam).

## 3. PROMOÇÕES (preço que o usuário mudou à mão no CONTROLE)
1. `promo_sync.py $W "<data hora>"` → `promo_req.json`, `promo_upload.json`, `promo_resumo.txt`.
2. Se houver mudança: `update_spreadsheet` com `promo_req.json` (C texto com ponto, K/L conferência, P data e preço antigo) e
   `promo_excel.py $W $W/Promocao_TikTok_<AAAAMMDD>.xlsx` (vai anexado no e-mail).
   SKU com preço do CONTROLE ≥ preço cheio não é atualizado (o TikTok recusa): ele aparece no e-mail.

## 4. Preço x canais
`canais.py $W "<dd/mm/aaaa>" $W/anterior.json` → `canais.json`, `canais_resumo.txt` (só percentuais e o porquê; "mesmo preço" = até 1%).

## 5. Produtos novos fora do TikTok
1. `novos.py $W "<dd/mm/aaaa>" "<data da linha anterior do RESUMO, se houver>"` → `novos.json`, `novos_resumo.txt`.
   Usa o relatório de produtos mais recente em `.claude/skills/tiktok-relatorios-navegador/entrada/` se existir.
2. Reescreva `'PRODUTOS NOVOS FORA DO TIKTOK'!A4:G` (limpe com `batch_clear_values` e grave a lista) e B2 = data/hora.

## 6. Pedidos baixados de dia (→ ANÁLISE)
Se existir em `.claude/skills/tiktok-relatorios-navegador/entrada/` um `pedidos_*.csv` mais novo que o último registrado na
col. N do RESUMO DIÁRIO (texto "… (pedidos_AAAAMMDD_HHMM)"), siga o roteiro `/tiktok-pedidos` com esse arquivo
(`.claude/skills/tiktok-pedidos/SKILL.md`): só a ANÁLISE, nunca a CONCILIAÇÃO. Se não houver arquivo novo, diga no e-mail
que os pedidos do dia não foram baixados.

## 7. Registro
- `'HISTÓRICO CUSTO TIKTOK'!B2:D2` = `[["<data hora>","Situação:","OK – <resumo curto>"]]` ou `"INCOMPLETA – <motivo>"`.
- `append_values` em `'RESUMO DIÁRIO TIKTOK'!A2:N` com uma linha: data, shopee (3 %), comparados, ml (3 %), comparados,
  pendentes novos, custos alterados, alertas, linhas da PROMOÇÕES alteradas, "<n> (pedidos_…)" ou "—".

## 8. E-mail único (sempre, exceto quando o passo 0 parar)
Assunto: `[TikTok] Rotina <dd/mm> – <a> reajuste(s), <p> preço(s) p/ subir, <n> produto(s) novo(s)`
(se algo falhou, comece com `[TikTok] ATENÇÃO:`). Corpo em `htmlBody` (e `body` em texto puro, sem Markdown), nesta ordem:
1. Custo (resumo.txt) – tabela com os alertas de reajuste.
2. PROMOÇÕES (promo_resumo.txt) – com o Excel anexado (`attachments`, referência de arquivo local
   `sha256:<hash>:<caminho>`; calcule com `sha256sum`).
3. Preço x canais (canais_resumo.txt) – só percentuais e o porquê.
4. Produtos novos fora do TikTok (novos_resumo.txt).
5. Pedidos/ANÁLISE: quantos novos, margem estimada, cancelados/devolvidos; ou o aviso de que não houve download.
Link: https://docs.google.com/spreadsheets/d/1ZpeObRddsYOU6lphQaRuH2j4O_dgEzCUdV4ODTxst9w

## 9. Mensagem final
Resumo curto. Não faça commit nem push (a não ser que o usuário peça).

## Manutenção
`dados/mapa.json` = SKU → código no Bling (+ kits). SKU novo no CONTROLE precisa entrar nele (depois de `/tiktok-novos-produtos`).
