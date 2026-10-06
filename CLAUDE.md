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
- A linha amarela 414 separa os 20 produtos criados em 06/10/2026.
- Cores da margem (col. M): vermelho abaixo de 10%, amarelo de 10% a 15%, verde a partir de 15%.

### Aba BASE PRODUTOS TIKTOK

- É uma cópia do arquivo `all_information_template` do TikTok Seller Center, sem descrição, quantidade e colunas de imagem.
- A = ID do produto, G = ID do SKU, K = SKU do vendedor (= SKU Bling). Os três ficam em texto, porque os IDs têm 19 dígitos.
- U = linha no CONTROLE. A fórmula compara com `VALUE()`, porque o SKU pode vir com zero à esquerda.
- V = DATA DE ENTRADA, no formato dd/mm/aaaa.

### Aba PROMOÇÕES TIKTOK

- Segue o modelo `FixedPriceWithSKU`.
- A = Product_id, B = SKU_id, C = Preço da oferta em texto com **ponto** (ex.: `35.90`).
- D e E ficam vazias, só com o cabeçalho.
- Sempre **valores colados, nunca fórmula**.
- As colunas G a M são só conferência. O Excel enviado ao usuário tem apenas A a E, montado sobre o modelo original.

## Regras de preço

- **Custo:** fornecedor **padrão** no Bling (`listProductSuppliers`, `padrao=true`).
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
- **Promoção:** a oferta precisa ser **menor** que o preço original. Se o preço de venda for igual ao cheio, o produto precisa de ajuste de preço.

## Processo quando chegar uma nova planilha de produtos do TikTok

1. Compare com a BASE PRODUTOS TIKTOK pelo ID do SKU e identifique só os SKUs novos.
2. Adicione os novos na BASE com a DATA DE ENTRADA do dia.
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

## Histórico

- **06/10/2026:**
  - Base criada com 161 SKUs (109 produtos).
  - 20 SKUs que não estavam no CONTROLE foram criados (linhas 415 a 434).
  - Promoção gerada com os 161 SKUs.
  - SKU 9301 ajustado para R$ 35,90 (20% de margem).
