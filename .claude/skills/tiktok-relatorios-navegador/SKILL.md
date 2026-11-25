---
name: tiktok-relatorios-navegador
description: Baixa pelo navegador do computador do usuário (TikTok Shop Seller Center Brasil) o relatório de pedidos e o modelo de produtos (todas as informações), na pasta Downloads. Roda às 10h30, com nova tentativa às 15h, só quando o computador está ligado; se não conseguir, avisa por e-mail. Use quando a tarefa agendada disparar ou quando o usuário pedir "baixa os relatórios do TikTok" ou /tiktok-relatorios-navegador.
---

# Relatórios do TikTok Shop pelo navegador (ensinado pelo usuário em 25/11/2026)

**Status:** passo a passo recebido; ainda NÃO testado (o computador não estava conectado à sessão em 25/11).

## Pré-requisitos
- Computador do usuário ligado, com o app Claude para desktop e o Remote Control ativo, compartilhando a pasta **Downloads**.
- Navegador já logado em https://seller-br.tiktok.com/ (se pedir login ou código de verificação, pare: o usuário precisa refazer o login).
- Antes de usar o navegador, carregue a skill do navegador (`anthropic-skills:built-in-browser` ou `anthropic-skills:chrome-browser`).

## Quando roda
- 10h30 (horário de Brasília). Se falhar ou o computador estiver desligado, nova tentativa às 15h.
- Se às 15h também não der: pule o dia e mande e-mail (Gmail) para lbandeira2029@gmail.com, cc lbandeira2029.cursos@gmail.com,
  assunto `[TikTok] Relatórios do dia NÃO baixados – <dd/mm>`, dizendo o motivo (computador desligado, login expirado, erro na página).

## Relatório de pedidos (vendas)
1. Abrir https://seller-br.tiktok.com/
2. Menu **Pedidos > Gerenciar pedidos**.
3. Clicar na aba **Todos**.
4. **Exportar** → **Pedidos filtrados** → todos.
5. Formato: **CSV** (o `/tiktok-pedidos` já lê CSV; se não houver, Excel).
6. O arquivo leva de segundos a minutos para ser gerado. Depois clicar em **Baixar**.
   O item que ainda não foi baixado fica com uma **bolinha vermelha**: baixe o mais recente com a bolinha.
7. Conferir que o arquivo `Todos_pedido-*.csv` (ou .xlsx) apareceu em Downloads.

## Relatório de produtos
1. Menu **Produtos > Ações em massa > Editar produtos**.
2. Selecionar **Todos os produtos** e **Todas as informações**.
3. **Gerar modelo**. Demora um pouco para carregar.
4. Depois clicar em **Baixar** (arquivo `all_information_template*.xlsx` em Downloads).

## Depois do download (de dia, sem planilha: o trabalho pesado fica para a madrugada)
1. Copie os dois arquivos do Downloads do computador para o container (pasta nova no scratchpad).
2. `python3 -I .claude/skills/tiktok-relatorios-navegador/scripts/extrair.py <pedidos.csv> <produtos.zip|xlsx> <AAAAMMDD_HHMM>`
   Gera em `entrada/` só as colunas usadas (pedidos **sem** CPF, nome, telefone, endereço; produtos com IDs, SKU, nome, preço).
3. `git add .claude/skills/tiktok-relatorios-navegador/entrada && git commit` e `git push` na branch claude/brave-gates-3etn2o
   (é assim que a rotina da madrugada recebe os arquivos).
4. Não grave na planilha de dia. A rotina das 3h01 roda o `/tiktok-pedidos` (ANÁLISE) e compara os produtos com o CONTROLE.
5. Se o download funcionou, não precisa e-mail de dia. Se falhou às 15h, mande o aviso descrito em "Quando roda".
