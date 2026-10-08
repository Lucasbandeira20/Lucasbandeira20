---
name: tiktok-novos-produtos
description: Processa uma nova exportação de produtos do TikTok Seller Center (arquivo all_information_template .xlsx) da Avelar Shop. Identifica os SKUs novos, adiciona à BASE PRODUTOS TIKTOK, busca custo e preço no Bling, calcula o preço de venda pelas regras e cria as linhas no CONTROLE. Depois monta a PROMOÇÕES e gera o Excel de upload da promoção (FixedPriceWithSKU). Use sempre que o usuário enviar uma planilha/exportação de produtos do TikTok, disser "nova planilha do TikTok", "novos produtos do TikTok", "subi mais produtos" ou pedir /tiktok-novos-produtos.
---

# Novos produtos TikTok Shop → BASE, CONTROLE, PROMOÇÕES e Excel

As regras de preço, colunas e histórico estão no `CLAUDE.md` da raiz do repositório e na aba
**REGRAS E PROCESSO TIKTOK**. Leia o CLAUDE.md antes de começar. Este arquivo é o roteiro de execução.

- Planilha: `1ZpeObRddsYOU6lphQaRuH2j4O_dgEzCUdV4ODTxst9w` (locale pt-BR: fórmulas com `;`).
- sheetIds: CONTROLE `236203424`, BASE `1703248089`, PROMOÇÕES `293760526`, REGRAS `738877884`.
- Nunca altere abas de Mercado Livre, Shopee ou Site. Elas só são lidas para referência.
- Scripts: `.claude/skills/tiktok-novos-produtos/scripts/` (rodar com `python3 -I`). Pasta de trabalho do
  lote (`$L`): uma pasta nova no scratchpad, ex.: `$SCRATCH/lote_AAAAMMDD_HHMM`. Copie o .xlsx enviado para lá.
- Se o usuário pedir "analisa e me fala primeiro", pare depois do passo 3 e mostre o resumo.
- Mantenha o usuário informado com frases curtas entre as etapas (ex.: "BASE gravada; consultando o Bling").

## Passo 0: carimbo do lote
- Data e hora do lote: `TZ=America/Sao_Paulo date '+%d/%m/%Y %H:%M'`. Todos os SKUs do arquivo recebem a mesma.
- Escolha uma cor de fundo nova (diferente das já usadas, ver CLAUDE.md). Sugestões em ordem:
  amarelo-claro `{1, 0.949, 0.8}`, azul-esverdeado `{0.816, 0.937, 0.937}`, rosa `{0.988, 0.894, 0.925}`,
  cinza-azulado `{0.871, 0.894, 0.922}`, verde-limão `{0.902, 0.957, 0.824}`.

## Passo 1: quais SKUs são novos
1. Leia com `get_values` (salve cada resultado com `scripts/salvar_resultado.py "<range>" <arquivo>`):
   - `'BASE PRODUTOS TIKTOK'!G1:G3000` → `$L/base_G.json`
   - `'CONTROLE ANÚNCIOS TIKTOKSHOP 03.10'!C1:C3000` → `$L/controle_C.json`
   - Anote também a última linha preenchida da BASE (= início do lote), da PROMOÇÕES e do CONTROLE
     (leia `A1:A3000` da PROMOÇÕES e `B1:C3000` do CONTROLE, só para achar o fim).
2. `python3 -I scripts/novos.py $L/<arquivo>.xlsx $L/base_G.json $L/controle_C.json $L`
   - Gera `novos.json`, `skus_todos.json` e `skus_criar.json`, e imprime o resumo. Ele avisa SKUs Bling em mais de um
     anúncio e quantos SKUs sumiram da exportação (anúncios removidos no TikTok).
   - Se não houver novos, avise o usuário e pare.

## Passo 2: Bling (custo e preço cheio)
- Até ~20 SKUs: faça você mesmo. `listProducts` com `codigos` (lote de até 100), `criterio "5"` e
  fields `id,codigo,preco,situacao,formato,precoCusto`. Depois `listProductSuppliers(idProduto)` de cada SKU a criar
  e use o fornecedor `padrao=true` (`precoCusto`; se 0, `precoCompra`).
- Mais que isso: um subagente (general-purpose), com o prompt da seção "Prompt do Bling" abaixo.
- **SKU que não volta na consulta em lote:** busque só ele (`codigos:[sku]` com `criterio "1"` e `"5"`, e por `nome`).
  O 16859 não voltou em lote mas existia. Só considere "não existe" depois disso.
- **Kit (formato "E" ou nome "Par…"/"Kit…") com custo 0:** `getProduct` → composição; custo =
  Σ quantidade × custo do fornecedor padrão de cada componente; registre "2x SKU 123 + 1x SKU 456".
- **Inativo sem fornecedor:** use o `precoCusto` do cadastro e anote.
- Grave `$L/bling.json`: `{"<sku>": {"preco": n, "custo": n, "situacao": "A|I", "formato": "S|E", "kit": "", "nota": ""}}`.
- Cota: a API tem limite diário (zera à meia-noite) e por segundo. Em erro 429, espere 60 s. Se a cota diária acabou,
  avise o usuário e agende a continuação para 00:01 com `send_later`.

## Passo 3: referências e preço
1. Leia as abas de referência com `get_values` e salve em `$L/refs/` (só leitura):
   - `'Regra Especial Shopee AGO2026'!A1:J3000` → `refs/regra_especial.json`
   - `'Controle Anúncios Shopee'!A1:P3000` → `refs/shopee.json`
   - `'Regra Shopee Padrão'!A1:N3000` → `refs/regra.json`
   - `'Shopee TANKE'!A1:N3000` → `refs/tanke.json`
   - `'Cálculo de Margem 0203'!A1:L3000` → `refs/ml.json`
2. `python3 -I scripts/refs.py $L`: imprime SEM REF, APROX (nome aproximado) e DUPLICADO NA REGRA ESPECIAL.
3. `python3 -I scripts/precos.py $L`: aplica as regras e gera `linhas.json`, com o resumo por produto.
   - Flags: `!` ajuste especial, `S` sem referência, `U` subido para 10%.
   - Confira o resumo. Avise o usuário de casos estranhos, por exemplo um canal abaixo do custo (Cinta H10 Red), um
     custo que parece errado ou um preço quebrado (ex.: R$ 129,01 vindo do ML).

## Passo 4: gravar na planilha
`python3 -I scripts/payloads.py $L` gera `$L/payload/`. Escreva com `update_values`, passando os valores
exatamente como estão nos arquivos (IDs e SKUs como texto, números como número). Para muitas linhas, use um
subagente por grupo de arquivos, que imprime o JSON compacto e chama `update_values`.

**BASE** (linhas `b0`..`b1`, a partir da primeira vazia):
1. Se faltar grade, use `appendDimension` (BASE e PROMOÇÕES têm grade própria).
2. Use `copyPaste` com `PASTE_FORMAT` da última linha do lote anterior (A:V) para as novas, para manter o J como moeda.
   Depois aplique `repeatCell` com a cor nova em A:V.
3. Use `copyPaste` com `PASTE_FORMULA` da coluna U (fórmula "linha no CONTROLE") para as novas.
4. Grave `base_partN.json` em `A{b0}:T…`.
5. Grave a data em `V{b0}` e use `copyPaste` com `PASTE_VALUES` para o resto. Formato `dd/mm/yyyy hh:mm`.

**CONTROLE** (tabela "TABELA TIKTOKSHOP_2"; ela vai até a linha 1281):
1. Se o lote passar do fim da tabela, aumente a grade e a tabela antes. Confira o range da tabela com
   `get_spreadsheet` (fields `sheets.tables.range`).
2. Para a faixa amarela, use `copyPaste` com `PASTE_NORMAL` da linha 1190 (faixa vazia) para a 1ª linha livre `d`.
3. Use `copyPaste` com `PASTE_NORMAL` de uma linha de produto do último lote para `d+1 … d+n`. Isso copia fórmulas,
   validação e formatação condicional.
4. Aplique `repeatCell` com `numberFormat TEXT` em C`d+1`:C`d+n`, por causa do zero à esquerda.
5. Grave `ctl_BC → B:C`, `ctl_E → E`, `ctl_L → L`, `ctl_N → N`, `ctl_T → T` e `ctl_ZA → Z:AA`.
6. Leia de volta `C` e `L` do bloco e confira com o `linhas.json`.

**PROMOÇÕES** (mesmas linhas da BASE, `b0`..`b1`):
1. Grave na linha `b0` as fórmulas abaixo (troque `{r}` pelo número da linha).
2. Copie o formato da última linha do lote anterior. Copie a linha `b0` para as demais com `PASTE_FORMULA` e aplique
   a cor do lote.
   ```
   A ='BASE PRODUTOS TIKTOK'!A{r}
   B ='BASE PRODUTOS TIKTOK'!G{r}
   C =SUBSTITUTE(TEXT(INDEX('CONTROLE ANÚNCIOS TIKTOKSHOP 03.10'!L:L;'BASE PRODUTOS TIKTOK'!U{r});"0.00");",";".")
   D, E, F vazias
   G ='BASE PRODUTOS TIKTOK'!C{r}
   H ='BASE PRODUTOS TIKTOK'!H{r}
   I ='BASE PRODUTOS TIKTOK'!K{r}
   J =INDEX('CONTROLE ANÚNCIOS TIKTOKSHOP 03.10'!N:N;'BASE PRODUTOS TIKTOK'!U{r})
   K =INDEX('CONTROLE ANÚNCIOS TIKTOKSHOP 03.10'!L:L;'BASE PRODUTOS TIKTOK'!U{r})
   L =IF(OR(J{r}="";K{r}="");"";J{r}-K{r})
   M =IF(K{r}="";"SEM PREÇO";IF(K{r}<'BASE PRODUTOS TIKTOK'!J{r};"OK";"OFERTA >= PREÇO ORIGINAL"))
   N ='BASE PRODUTOS TIKTOK'!V{r}
   ```
3. Leia `A{b0}:N{b1}` e confira: tudo "OK", IDs com 19 dígitos e preço com ponto.
4. Cole como **valores** (`copyPaste` `PASTE_VALUES` sobre o próprio bloco). A aba nunca fica com fórmula.
5. SKU fora da promoção (`fora` no `linhas.json`, ou sem custo): limpe C e escreve em M o motivo ("FORA: …").

## Passo 5: Excel e entrega
1. Leia `'PROMOÇÕES TIKTOK'!A{b0}:C{b1}`, salve com `salvar_resultado.py` em `$L/promo_AC.json`.
2. `python3 -I scripts/excel.py $L/promo_AC.json $L/PROMOCOES_TIKTOK_<dd-mm-aaaa_hhmm>.xlsx`. Ele recusa IDs fora de
   19 dígitos ou preço com vírgula e ignora linhas sem preço.
3. Envie o arquivo com `SendUserFile` (`display: attach`).

## Passo 6: histórico
1. Na aba REGRAS, use `insertDimension` de 1 linha logo após o último lote do HISTÓRICO e escreva em A:B
   "data hora" + resumo.
2. No `CLAUDE.md`, atualize:
   - a lista de faixas amarelas;
   - a lista de cores/linhas da BASE;
   - o "Histórico".
3. Faça commit e push no branch de trabalho.
4. Responda ao usuário em português, curto:
   - números (novos, já no CONTROLE, criados, menor canal, 10%, 15%, ajustes, fora);
   - linhas usadas;
   - pontos para conferir: sem referência, nome aproximado, duplicados na Regra Especial, inativos, kits, preços
     quebrados e canal abaixo do custo.

## Prompt do Bling (subagente)
> Consulta somente leitura no Bling (não crie nem altere nada). No máximo 2 chamadas em paralelo; em 429 espere 60 s
> (até 5x). Entradas: A=`$L/skus_todos.json` (precisa id, preco, situacao, formato), B=`$L/skus_criar.json`
> (também custo). Ferramentas: ToolSearch "select:mcp__BLING__listProducts,mcp__BLING__listProductSuppliers,mcp__BLING__getProduct".
> 1) listProducts `codigos` em lotes de 100, criterio "5", fields [id,codigo,preco,situacao,formato,precoCusto];
> para os que faltarem, repita um a um com criterio "1" e "3" e com/sem zero à esquerda. 2) Para cada código de B:
> listProductSuppliers(idProduto), vínculo padrao=true, custo = precoCusto (se 0, precoCompra); listar vínculos por
> fornecedor economiza chamadas; sem vínculo → precoCusto do produto, anotar em nota. 3) Custo 0 e composição
> (formato "E" ou nome "Par "/"Kit ") → getProduct, custo = Σ qtd × custo padrão dos componentes, kit = "2x SKU … + 1x SKU …".
> Saída: `$L/bling.json` {"<sku>": {id, preco, situacao, formato, custo, kit, nota}, "_missing": [...]}.
> Relate contagens, inativos, kits e o que faltou.

## Lições dos lotes anteriores
- A exportação nova pode mudar colunas. Por isso `novos.py` mapeia pelo nome do cabeçalho, não pela posição.
- O SKU pode ter zero à esquerda (004460, 05222). A fórmula da BASE usa `VALUE()` e a coluna C do CONTROLE fica em TEXT.
- `TEXT(x;"0.00")` no pt-BR devolve vírgula. Por isso a fórmula usa `SUBSTITUTE` para o ponto.
- Máscara de campos (`fields`) do Sheets não aceita parênteses. Use listas separadas por vírgula.
- Ao formatar colunas de preço da BASE, copie o formato da linha anterior. `0.##` mostra "599,".
- Leia a regra de oferta contra o **preço do TikTok** (coluna J da BASE), não só contra o preço cheio do Bling.
- Subagente: diga exatamente quais ranges ele pode escrever e peça leitura de volta. Confira você mesmo depois,
  porque o relato do subagente pode errar a linha.
