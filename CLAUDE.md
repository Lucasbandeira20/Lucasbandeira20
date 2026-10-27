# Precificação e promoções TikTok Shop (Avelar Shop)

Fonte principal das regras: aba **REGRAS E PROCESSO TIKTOK** da planilha abaixo. Leia-a antes de começar e mantenha as duas cópias iguais.

## Planilha

- **CALCULO DE MARGEM CLAUDE 03/10/2026**
- ID: `1ZpeObRddsYOU6lphQaRuH2j4O_dgEzCUdV4ODTxst9w`
- Locale pt-BR: fórmulas usam `;` e vírgula decimal.
- Nunca altere as abas de Mercado Livre e Shopee. Trabalhe só nas abas do TikTok.
- Antes de qualquer mudança grande, mostre o plano ao usuário. Ele costuma pedir "analisa e me fala primeiro".

| Aba | sheetId | Uso |
|---|---|---|
| CONTROLE ANÚNCIOS TIKTOKSHOP 03.10 | 236203424 | Cálculo de margem e preço de todos os produtos. Chave: SKU Bling (col. C) |
| BASE PRODUTOS TIKTOK | 1703248089 | Produtos já anunciados no TikTok |
| PROMOÇÕES TIKTOK | 293760526 | Arquivo de upload de promoção |
| REGRAS E PROCESSO TIKTOK | 738877884 | Regras e histórico |
| Regra Especial Shopee AGO2026 | 1761605422 | Referência principal de preço Shopee |
| CAMPANHAS TIKTOK | 1765579766 | Seleção de produtos para campanhas com cupom (análise, não altera o CONTROLE) |
| ANÁLISE MARGEM VENDAS TIKTOK | 1935682352 | Margem real das vendas (a definir) |
| TOP 100 BLING x TIKTOK | 2026102701 | Os 100 produtos pai mais vendidos no Bling x vendas e margem no TikTok (só análise) |

### Aba CONTROLE ANÚNCIOS TIKTOKSHOP 03.10

Fica dentro da tabela "TABELA TIKTOKSHOP_2".

| Coluna | Conteúdo |
|---|---|
| A | FEITO (caixinha) |
| B | Produto |
| C | SKU, em texto |
| D | Tipo |
| E | Custo |
| F | Plataforma |
| G | Tarifa |
| H | Taxa |
| I | Imposto |
| J | Frete 6% |
| K | Custo total |
| L | **Valor de venda** |
| M | Margem |
| N | Preço cheio (Bling) |
| O | Desconto R$ |
| P | TT x ML |
| Q | TT x Shopee |
| R | Vencimento |
| S | Loja |
| T | OBS |
| U | Afiliados -8% |
| V | Margem afiliados |
| W | Preço sugerido |
| X | Margem alvo |
| Y | Análise |
| Z | Preço ML (ref) |
| AA | Preço Shopee (ref) |

- Linhas laranja são divisórias.
- Faixas amarelas separam os lotes de produtos criados: linha 414 (20 produtos de 06/10/2026 14:15), linha 435 (134 produtos do lote 06/10/2026 22:35, linhas 436 a 569) linha 570 (430 produtos do lote 07/10/2026 13:42, linhas 571 a 1000) linha 1001 (188 produtos do lote 07/10/2026 18:44, linhas 1002 a 1189) linha 1190 (12 produtos do lote 07/10/2026 23:39, linhas 1191 a 1202) e linha 1203 (29 produtos do lote 09/10/2026 18:03, linhas 1204 a 1232). A tabela vai até a linha 1281: expanda antes de um lote grande.
- Kits (ex.: "Par de pneus"): a coluna OBS (T) registra a composição usada no custo.
- Cores da margem (col. M): vermelho abaixo de 10%, amarelo de 10% a 15%, verde a partir de 15%.

### Aba BASE PRODUTOS TIKTOK

- É uma cópia do arquivo `all_information_template` do TikTok Seller Center, sem descrição, quantidade e colunas de imagem.
- A = ID do produto, G = ID do SKU, K = SKU do vendedor (= SKU Bling). Os três ficam em texto, porque os IDs têm 19 dígitos.
- U = linha no CONTROLE. A fórmula compara com `VALUE()`, porque o SKU pode vir com zero à esquerda.
- V = DATA E HORA DE ENTRADA, no formato dd/mm/aaaa hh:mm. SKUs que entram na mesma planilha recebem a mesma data e hora.
- Cada lote novo recebe uma cor de fundo diferente (o lote de 06/10/2026 22:35 é azul claro, linhas 163 a 377; o de 07/10/2026 13:42 é verde claro, linhas 378 a 867; o de 07/10/2026 18:44 é lilás, linhas 868 a 1107; o de 07/10/2026 23:39 é pêssego, linhas 1108 a 1131; o de 09/10/2026 18:03 é amarelo-claro, linhas 1132 a 1162).

### Aba PROMOÇÕES TIKTOK

- Segue o modelo `FixedPriceWithSKU`.
- A = Product_id, B = SKU_id, C = Preço da oferta em texto com **ponto** (ex.: `35.90`).
- D e E ficam vazias, só com o cabeçalho.
- Sempre **valores colados, nunca fórmula**.
- As colunas G a M são só conferência. A coluna N é a DATA E HORA DE ENTRADA, igual à da BASE.
- A coluna O é o LOTE / CAMPANHA NO TIKTOK (campanha de desconto em que o SKU está):
  - LOTE 1 (linhas 2 a 162): PROMO-LUCASB-06.10.26-01.10.27;
  - LOTE 2 (163 a 377): PREÇOFIXO-LUCASB-07.10.26-01.10.27;
  - LOTE 3 (378 a 867): PREÇOFIXO-LUCASB-07.10.26-01.10.27 | LOTE3 (a "- LOTE 3" foi desativada);
  - LOTE 4 (868 a 1107): … | LOTE4; LOTE 5 (1108 a 1131): … | LOTE5; LOTE 6 (1132 a 1162): … | LOTE6.
- O Excel enviado ao usuário tem apenas A a E, montado sobre o modelo original.

### Aba CAMPANHAS TIKTOK

- Só análise. **Nunca altere o CONTROLE** por causa de campanha: os preços oficiais ficam lá.
- C2 = desconto da campanha (hoje 5%). Preço campanha = ROUNDDOWN(preço hoje × (1 − C2); 2). As margens são fórmulas, iguais às do CONTROLE.
- **Estoque vem antes da análise.** Para qualquer lista de campanha, consulte primeiro o estoque no Bling (`listProducts` com `codigos`, field `estoque` → `saldoVirtualTotal`). SKU com estoque 0 não entra na campanha. Ordene a lista pelo **maior estoque**.
- Pares e kits (formato "E") têm estoque virtual, calculado pelos pneus avulsos. Pares que usam o mesmo pneu dividem esse estoque.
- Lista atual (escolhida pelo usuário em 08/10/2026): linhas 6 a 37, com 32 SKUs ordenados por estoque (19572 e 19579 retirados a pedido). Os SKUs com estoque 0 (004460 e 22812) foram retirados. Col. P = estoque Bling. Col. Q = DATA E HORA DE ENTRADA na campanha (dd/mm/aaaa hh:mm; o lote atual é 08/10/2026 10:19). Itens que entrarem juntos recebem a mesma data e hora.
- **Inscrição na campanha:** use o arquivo que o TikTok gera no painel (`..._batch_campaign_template_*.xlsx`), **com o mesmo nome e o mesmo formato**. Ele vem com todos os SKUs ativos e com o preço sugerido (preço atual − R$ 0,50) nas colunas de cada campanha. Apague as linhas que não entram e troque só os preços das colunas de campanha (texto com ponto). Não mexa no resto. Feito em 08/10/2026: 32 SKUs nas duas campanhas 10.10 (Flash Sale e Monthly Sale).
- Preço hoje e custo são cópia do CONTROLE em 08/10/2026. Col. O = linha no CONTROLE.

### Aba TOP 100 BLING x TIKTOK

- Só análise: mostra o que acelerar no TikTok. **Não altera o CONTROLE.**
- Fonte: relatório de vendas do Bling exportado pelo usuário (Data, Cliente, Produto, Quantidade, Venda Líquida; **sem SKU**). Usar **o período inteiro do relatório** (hoje 01/08 a 27/10/2026), com uma coluna extra para os últimos 30 dias. Variações agrupadas pelo nome do pai (corta o nome em " Cor:", " Tamanho:", " Tamanho do Quadro:" etc.).
- **Nome → SKU e estoque: sempre pelo Bling** (`listProducts` com `nome`, que busca pelo começo do nome; use prefixos curtos como "Pedivela", "Suspensão" para trazer vários de uma vez). Produto com variação: o pai (formato V) dá o SKU pai; o estoque é a soma das variações. Nome antigo e nome novo do mesmo produto (ex.: Athor Mist) são somados. Só entram produtos com estoque > 0. O CONTROLE só é usado depois, pelo SKU, para preço, custo e margem.
- D2 = vendas mínimas no TikTok para "boa venda" (5 un.). D3 = margem mínima para baixar preço ou entrar em campanha (15%). D4 = cobertura mínima de estoque para acelerar (30 dias). Os três são editáveis.
- Col. I = cobertura de estoque em dias (estoque ÷ venda média diária dos últimos 30 dias no Bling). Col. J = anunciado no TikTok. Col. K = LOTE / CAMPANHA NO TIKTOK (vem da coluna O da PROMOÇÕES, pelo SKU; "—" se não está em promoção). Col. N = linha no CONTROLE; O, P e Q (preço, custo, margem) são fórmulas que buscam no CONTROLE. R = preço mínimo com margem de 10% (preço redondo, calculado). I, M, O a Q e S a W são fórmulas.
- Classificação (col. V), cor da linha por formatação condicional: verde = vende bem no TikTok; azul = acelerar, tem margem; vermelho = sem margem para baixar; cinza = não anunciado. Cobertura abaixo de D4 fica laranja e a ação sugerida manda repor antes de acelerar.
- Vendas TikTok (col. L) vêm da aba ANÁLISE MARGEM VENDAS TIKTOK, sem cancelados (valor colado em 27/10/2026).

## Regras de preço

- **Custo:** fornecedor **padrão** no Bling (`listProductSuppliers`, `padrao=true`).
- **Kits (composição, formato "E"):** o custo do kit no Bling vem zerado. Use a soma dos componentes (quantidade × custo do fornecedor padrão de cada um) e anote a composição na coluna OBS.
- **Preço cheio:** preço de venda do Bling (`listProducts` → `preco`). É igual ao preço de varejo do TikTok.
- **Preço de venda:** igual ao **menor** preço entre Shopee e Mercado Livre.
  - Shopee: aba Regra Especial. Lojas Avelar 14%; Caloi, Colli, Athor e Tanke 12% + R$12. Para produtos Tanke, usar o menor entre Avelar e a loja Tanke.
  - Mercado Livre: Clássico; se não houver, Premium.
- **Margem mínima:** 10%. Se ficar abaixo no preço do menor canal, sobe para o primeiro preço "redondo" que chega a 10%.
- **Sem referência** em Shopee e ML: margem de 15%.
- **Preços redondos:**
  - abaixo de R$50: final ,90;
  - a partir de R$50: múltiplo de 10 menos 0,01, 0,10, 1,10, 2,10, 4,50 ou 5,10.
- **Variantes** do mesmo produto têm o mesmo preço.
- **Afiliados:** não considerar por enquanto.
- **Taxas TikTok:**
  - comissão abaixo de R$50 = 10% + R$4; a partir de R$50 = 6% + R$6;
  - frete 6% (teto R$50);
  - imposto 7,3%.
  - Margem = 1 − (custo + taxas + imposto + frete) / preço.
- **Promoção:** a oferta precisa ser **menor** que o preço original. Se nem no preço cheio a margem chega a 10%, o SKU fica fora da promoção (ex.: 12022). Se o preço de venda for igual ao cheio, ajuste para margem de 20% (aplicado em 9301, 22309 e 20444).
- **Limite do Bling:** a API tem cota diária (zera à meia-noite) e limite por segundo. Consulte em lotes, com pausas.

## Processo quando chegar uma nova planilha de produtos do TikTok

Use a skill `/tiktok-novos-produtos` (`.claude/skills/tiktok-novos-produtos/`): ela tem o roteiro passo a passo e os scripts (comparação, referências, preços, payloads e Excel). Resumo:


1. Compare com a BASE PRODUTOS TIKTOK pelo ID do SKU e identifique só os SKUs novos.
2. Adicione os novos na BASE com a DATA DE ENTRADA do dia (coluna V). Na PROMOÇÃO, a data vai na coluna N.
3. Para cada SKU novo, verifique se já está no CONTROLE (pelo SKU Bling). Se não estiver:
   - busque o custo (fornecedor padrão) e o preço cheio no Bling;
   - calcule o preço pelas regras acima;
   - crie a linha no CONTROLE, abaixo de uma nova linha divisória amarela.
4. Monte a PROMOÇÃO **só com os SKUs novos**:
   - colunas A a E, valores colados, preço com ponto;
   - gere o Excel no modelo do TikTok.
5. Antes de entregar, confira:
   - oferta menor que o preço original;
   - nenhuma linha sem preço;
   - IDs com 19 dígitos, em texto.
6. Registre o que foi feito no HISTÓRICO da aba REGRAS E PROCESSO TIKTOK.

## Pendências (em aberto)

- Regra Especial Shopee tem 9 produtos duplicados com preços diferentes (ex.: Coroa SLX M675 24d R$ 89,00 × R$ 39,90). O usuário precisa dizer qual linha vale. Até lá, vale a primeira linha.
- Kit 3 Pneu Chaoyang Phantom Wet (18280) aparece com estoque de 4.931 no Bling, o que parece erro de cadastro. Precisa ser conferido.
- Próximas frentes: ANÁLISE DE MARGEM DA VENDA (aba ANÁLISE MARGEM VENDAS TIKTOK) e CONCILIAÇÃO FINANCEIRA. Precisam do relatório de pedidos e do de liquidação/repasse do TikTok.

## Histórico

- **06/10/2026:**
  - Base criada com 161 SKUs (109 produtos).
  - 20 SKUs que não estavam no CONTROLE foram criados (linhas 415 a 434).
  - Promoção gerada com os 161 SKUs.
  - SKU 9301 ajustado para R$ 35,90 (20% de margem).
- **06/10/2026 22:35 (2ª carga):**
  - 215 SKUs novos na BASE (linhas 163 a 377, fundo azul).
  - 81 já estavam no CONTROLE. Os outros 134 foram criados (linhas 436 a 569, abaixo da faixa amarela 435); 44 deles são kits com custo pela composição.
  - Promoção e Excel só com os 215 novos (PROMOÇÕES, linhas 163 a 377).
- **07/10/2026 13:42 (3ª carga):**
  - 490 SKUs novos na BASE (linhas 378 a 867, fundo verde claro).
  - 55 já estavam no CONTROLE. Os outros 430 foram criados (linhas 571 a 1000, abaixo da faixa amarela 570). Cinco SKUs Bling têm dois anúncios no TikTok (22786, 22596, 22359, 21625, 21622).
  - 411 no menor canal, 11 sem referência (15%), 4 subidos para 10%.
  - 19718, 19719 e 23645 (XC702 Prata, venda igual ao cheio) foram para R$ 1.279,90 (20%). 21770 foi para R$ 49,90 (Shopee acima do cheio de R$ 50).
  - 91 SKUs inativos no Bling, sem fornecedor (Shimano RC102, RC502, XC702 e RC903), usaram o custo do cadastro.
  - Promoção e Excel só com os 490 novos (PROMOÇÕES, linhas 378 a 867).
- **07/10/2026 18:44 (4ª carga, exportação com todos os ativos, 1101 SKUs):**
  - 240 SKUs novos na BASE (linhas 868 a 1107, fundo lilás). Os 5 anúncios duplicados da 3ª carga saíram do TikTok.
  - 51 já estavam no CONTROLE. Os outros 188 foram criados (linhas 1002 a 1189, abaixo da faixa amarela 1001).
  - 126 no menor canal, 44 subidos para 10%, 17 sem referência (15%). 22491 foi para R$ 31,90 (venda igual ao cheio, 20%).
  - 16859 não voltou na consulta em lote da API, mas existe no Bling: foi criado depois (linha 1189, R$ 224,90). Se um SKU não aparecer, confirme buscando só ele.
  - Fora da promoção: 12022 (margem de 7,9% até no preço cheio).
  - Promoção e Excel com 239 SKUs (PROMOÇÕES, linhas 868 a 1107).
- **07/10/2026 23:39 (5ª carga, 1125 SKUs ativos):**
  - 24 SKUs novos na BASE (linhas 1108 a 1131, fundo pêssego).
  - 12 já estavam no CONTROLE. Os outros 12 foram criados (linhas 1191 a 1202, abaixo da faixa amarela 1190).
  - 9 no menor canal, 2 sem referência (15%), 1 subido para 10% (22005, Cinta H10 Red: Shopee R$ 329,90 abaixo do custo).
  - Promoção e Excel com os 24 novos (PROMOÇÕES, linhas 1108 a 1131).
- **09/10/2026 17:58 (alteração de preço):**
  - Sapatilha Shimano SH-MX101 (22 SKUs, 23652 a 23673) passou de R$ 599,90 (20,3%) para R$ 514,90 (10,4% de margem), a pedido do usuário.
  - Atualizados: CONTROLE L576:L597 (com OBS na coluna T) e PROMOÇÕES C, K e L nas linhas 390 a 411. Não está na CAMPANHAS TIKTOK.
  - Excel de promoção não foi gerado. O usuário alterou o preço no TikTok (confirmado em 09/10/2026).
- **Alteração de preço avulsa:** atualize o CONTROLE (L + OBS com data e motivo), a PROMOÇÕES (C em texto com ponto, K e L) e a CAMPANHAS TIKTOK, se o SKU estiver lá. Registre no HISTÓRICO da aba REGRAS e aqui.
- **09/10/2026 18:03 (6ª carga, exportação em 2 arquivos, 1150 SKUs ativos):**
  - 31 SKUs novos na BASE (linhas 1132 a 1162, fundo amarelo-claro), todos Polar (relógios e cinta).
  - 2 já estavam no CONTROLE. Os outros 29 foram criados (linhas 1204 a 1232, abaixo da faixa amarela 1203).
  - 16 no menor canal, 9 ajustados para 20% (menor canal igual ao preço original), 2 subidos para 10%, 2 sem referência (15%).
  - 21992 (Unite Branco, linha 331) tinha venda igual ao cheio (R$ 1.899,00) e foi para R$ 1.499,90 (20%).
  - Saíram do TikTok: 6 Nathor Aro 12 Personagens e os 5 anúncios duplicados de selins.
  - Promoção e Excel com os 31 novos (PROMOÇÕES, linhas 1132 a 1162).
- **27/10/2026 (aba TOP 100 BLING x TIKTOK):**
  - Relatório de vendas do Bling de 01/08 a 27/10/2026 (40.813 linhas, 71.060 unidades). Ranking pelo período inteiro, com SKU e estoque buscados no Bling pelo nome.
  - Resultado: 23 vendem bem no TikTok, 46 têm margem para acelerar (13 com estoque para menos de 30 dias), 14 sem margem para baixar e 17 não anunciados.
  - Fora por estoque ≤ 0: Selim GTA Comfort 22800, Mova Way 4.0 23303, Cadeado Articulado GTA 23132, Freio Altus traseiro 12735, cubo TH390 32F, BB52 23427 e BB-MT501 18451.
  - Estoques muito altos de pneus Chaoyang e pares (ex.: 016855 com 14.882, par 17816 com 7.441) parecem erro de cadastro, como o 18280.
- **27/10/2026 (PROMOÇÕES, coluna O):** nova coluna LOTE / CAMPANHA NO TIKTOK, com o nome da campanha de cada lote (lotes 1 a 6, pela data de entrada da coluna N). Cupons e ofertas relâmpago encerradas não entram.
- **27/10/2026 (TOP 100, coluna K):** nova coluna LOTE / CAMPANHA NO TIKTOK, ao lado de "Anunciado no TikTok": 69 produtos no lote 1, 10 no lote 2, 1 no lote 3, 1 no lote 4, 2 no lote 5 e 17 não anunciados.
