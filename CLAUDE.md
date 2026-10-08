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
| ANÁLISE MARGEM VENDAS TIKTOK | 1935682352 | Margem real de cada venda × CONTROLE |
| CONCILIAÇÃO FINANCEIRA TIKTOK | 2026100801 | Resumo, transferências e repasse pedido a pedido |

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
- Faixas amarelas separam os lotes de produtos criados: linha 414 (20 produtos de 06/10/2026 14:15), linha 435 (134 produtos do lote 06/10/2026 22:35, linhas 436 a 569) linha 570 (430 produtos do lote 07/10/2026 13:42, linhas 571 a 1000) linha 1001 (188 produtos do lote 07/10/2026 18:44, linhas 1002 a 1189) e linha 1190 (12 produtos do lote 07/10/2026 23:39, linhas 1191 a 1202). A tabela vai até a linha 1281: expanda antes de um lote grande.
- Kits (ex.: "Par de pneus"): a coluna OBS (T) registra a composição usada no custo.
- Cores da margem (col. M): vermelho abaixo de 10%, amarelo de 10% a 15%, verde a partir de 15%.

### Aba BASE PRODUTOS TIKTOK

- É uma cópia do arquivo `all_information_template` do TikTok Seller Center, sem descrição, quantidade e colunas de imagem.
- A = ID do produto, G = ID do SKU, K = SKU do vendedor (= SKU Bling). Os três ficam em texto, porque os IDs têm 19 dígitos.
- U = linha no CONTROLE. A fórmula compara com `VALUE()`, porque o SKU pode vir com zero à esquerda.
- V = DATA E HORA DE ENTRADA, no formato dd/mm/aaaa hh:mm. SKUs que entram na mesma planilha recebem a mesma data e hora.
- Cada lote novo recebe uma cor de fundo diferente (o lote de 06/10/2026 22:35 é azul claro, linhas 163 a 377; o de 07/10/2026 13:42 é verde claro, linhas 378 a 867; o de 07/10/2026 18:44 é lilás, linhas 868 a 1107; o de 07/10/2026 23:39 é pêssego, linhas 1108 a 1131).

### Aba PROMOÇÕES TIKTOK

- Segue o modelo `FixedPriceWithSKU`.
- A = Product_id, B = SKU_id, C = Preço da oferta em texto com **ponto** (ex.: `35.90`).
- D e E ficam vazias, só com o cabeçalho.
- Sempre **valores colados, nunca fórmula**.
- As colunas G a M são só conferência. A coluna N é a DATA E HORA DE ENTRADA, igual à da BASE.
- O Excel enviado ao usuário tem apenas A a E, montado sobre o modelo original.

### Aba CAMPANHAS TIKTOK

- Só análise. **Nunca altere o CONTROLE** por causa de campanha: os preços oficiais ficam lá.
- C2 = desconto da campanha (hoje 5%). Preço campanha = ROUNDDOWN(preço hoje × (1 − C2); 2). As margens são fórmulas, iguais às do CONTROLE.
- **Estoque vem antes da análise.** Para qualquer lista de campanha, consulte primeiro o estoque no Bling (`listProducts` com `codigos`, field `estoque` → `saldoVirtualTotal`). SKU com estoque 0 não entra na campanha. Ordene a lista pelo **maior estoque**.
- Pares e kits (formato "E") têm estoque virtual, calculado pelos pneus avulsos. Pares que usam o mesmo pneu dividem esse estoque.
- Lista atual (escolhida pelo usuário em 08/10/2026): linhas 6 a 37, com 32 SKUs ordenados por estoque (19572 e 19579 retirados a pedido). Os SKUs com estoque 0 (004460 e 22812) foram retirados. Col. P = estoque Bling. Col. Q = DATA E HORA DE ENTRADA na campanha (dd/mm/aaaa hh:mm; o lote atual é 08/10/2026 10:19). Itens que entrarem juntos recebem a mesma data e hora.
- **Inscrição na campanha:** use o arquivo que o TikTok gera no painel (`..._batch_campaign_template_*.xlsx`), **com o mesmo nome e o mesmo formato**. Ele vem com todos os SKUs ativos e com o preço sugerido (preço atual − R$ 0,50) nas colunas de cada campanha. Apague as linhas que não entram e troque só os preços das colunas de campanha (texto com ponto). Não mexa no resto. Feito em 08/10/2026: 32 SKUs nas duas campanhas 10.10 (Flash Sale e Monthly Sale).
- Preço hoje e custo são cópia do CONTROLE em 08/10/2026. Col. O = linha no CONTROLE.

### Aba ANÁLISE MARGEM VENDAS TIKTOK

- Uma linha por pedido (enviados + a enviar), em ordem de data. Dados colados dos relatórios do TikTok; o resto é fórmula.
- A data | B pedido (texto) | C status | D situação financeira | E produto | F SKU | G qtd | H custo (fórmula, CONTROLE col. E) | I preço cheio | J desconto loja | K **valor de venda** (= I − J) | L desconto TikTok (pago pela plataforma, não entra na margem) | M pago pelo cliente | N comissão | O frete SFP 6% | P taxa por item | Q afiliados | R outras taxas | S imposto 7,3% | T custo produto | U custo total | V repasse TikTok | W **margem real** | X lucro | Y linha no CONTROLE | Z preço CONTROLE | AA margem CONTROLE | AB diferença | AC conferência (OK se ±0,5 p.p.) | AD motivo.
- Cores da margem (W e AA) iguais às do CONTROLE.

### Aba CONCILIAÇÃO FINANCEIRA TIKTOK

- Linhas 4 a 21: resumo das vendas (fórmulas sobre a ANÁLISE). Linhas 23 a 31: onde está o dinheiro (transferido, a receber, em devolução, sem extrato).
- Linhas 33 a 36: transferências do TikTok (aba Pagamentos do income) × soma dos pedidos do pagamento. Col. G = caixinha para conferir no extrato do banco.
- Linha 39 em diante: pedido a pedido. L = repasse esperado pela regra do CONTROLE; M = repasse do TikTok (real ou estimado); N = diferença. Inclui os pedidos cancelados que aparecem zerados nos extratos.

### Relatórios do TikTok usados

- **income (Detalhes do pedido / Extratos / Pagamentos):** o que já foi liquidado e transferido. O repasse é diário, no fim do dia, para a conta 54.050.***/****-52.
- **onhold:** o que ainda vai entrar (aguardando entrega, ou entregue + 7 dias). Os valores são estimados.
- **Todos_pedido (OrderSKUList):** status de todos os pedidos. Não traz taxas. Tem dados pessoais do cliente: não copiar para a planilha.
- Taxas conferidas em 08/10/2026: comissão 10% (< R$50) ou 6%, SFP 6% e taxa por item R$4 ou R$6 por unidade, iguais à regra do CONTROLE. ICMS e impostos vieram zerados.
- O onhold não tem as colunas "Taxa por item vendido" e "Taxa de anúncio de GMV Max": elas só aparecem somadas em "Taxas e impostos". A diferença entre esse total e o detalhe é o GMV Max (confirmado no painel em 08/10/2026). Na ANÁLISE ela vai na coluna R.

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
- **GMV Max (anúncios):** cobrança por pedido = (pagamento do cliente + desconto do TikTok) ÷ ROI do anúncio. Apareceu em 08/10 nas bicicletas 23620 (R$ 11,85, ROI 17,5) e 23622 (R$ 10,53, ROI 19,7), cerca de 5% a 5,7% da venda. Não está no CONTROLE. O usuário precisa decidir se o CONTROLE considera esse custo ou se tira do GMV Max os produtos com margem perto de 10%.
- Margem: comissão de afiliado (até 8,5%) não está no CONTROLE e derrubou várias vendas para baixo de 10%. O usuário precisa decidir se o CONTROLE passa a considerar afiliados.
- Atualizar a ANÁLISE e a CONCILIAÇÃO a cada novo download dos relatórios (income, onhold e pedidos).

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
- **08/10/2026 11:00 (análise de margem e conciliação):**
  - 138 vendas (116 enviadas + 22 a enviar) nas abas ANÁLISE MARGEM VENDAS TIKTOK e CONCILIAÇÃO FINANCEIRA TIKTOK (nova).
  - Margem média real de 13,1%. 44 vendas ficaram abaixo de 10% (preço antigo antes do ajuste de 06/10, afiliados e desconto extra de R$ 5). 45 vendas conforme o CONTROLE.
  - Transferências de 07/10 (R$ 16,08) e 08/10 (R$ 691,63) bateram com a soma dos pedidos. A receber: R$ 9.975,48.
