# Passagem de contexto — Vídeos China Academy (Solver)

Cole este documento no início de uma conversa nova e anexe os arquivos citados em "Arquivos para anexar".

## Quem e o quê

- Cliente: Avelar Shop / Solver. Produto: curso **China Academy** (importação da China).
- Professores:
  - **Felipe Avelar**, CEO Grupo Avelar
  - **Renan Arnoni**, CEO Arnoni Fitness
  - **Marcelo Alves**, Diretor de E-commerce da Avelar Shop · Sócio da Solver
- Curso: 5 encontros de 2h, plano de importação de 90 dias. Presencial na Solver (Av. Manoel Martins, 491, 10º andar, Conselheiro Lafaiete/MG), ao vivo online e gravado. Turmas à noite ou no sábado de manhã. WhatsApp (31) 98754-5544.
- Módulos:
  1. Estratégia e escolha do produto
  2. Fornecedores e negociação
  3. Custo real e tributação
  4. Logística, câmbio e capital de giro
  5. Marca própria, escala e plano de ação
- Grafia correta: **Solver** (não "Sober"/"Souver"), **Conselheiro Lafaiete** (não "Lafayette").

## Identidade visual (recriar igual)

- Fundo escuro `#0c0c0c` a `#141414`. Vermelho principal `#E4262D`. Vermelho de destaque em vídeo `#FF3B41`. Vermelho de borda `#B81A1F`/`#C21E24`. Verde de status `#3DDD83`.
- Fontes (Google Fonts):
  - **Urbanist** 500–900 (títulos em 800, letter-spacing −0.04em; caixa alta espaçada 0.14–0.34em para tarjas/selos)
  - **Noto Serif SC** 900 para 中国 / 巴西 / 登机牌 / 上海
  - **JetBrains Mono** 700 (painel de voo)
  - **Inter** 900 (SHA / BRA / 01)
- Elementos já criados (estão no `elementos-video.zip` do usuário; se faltar, recriar em HTML + Playwright com fundo transparente, escala 2x):
  - Títulos: "Da fábrica na China ao seu estoque.", "A importação é a sobrevivência do seu negócio." (palavra-chave em vermelho)
  - Tarja vermelha inclinada (−2°) e tarja reta em loop: `中国 ✦ NOVA TURMA ✦ PRESENCIAL + AO VIVO ✦ VAGAS LIMITADAS ✦ 巴西`
  - Logo "中国 CHINA • ACADEMY", título "CHINA • ACADEMY", 中国 grande
  - Selo pílula com borda vermelha, selo giratório circular
  - Números (5×2h, 90 dias, Ao vivo), linha do tempo 01–05, cards de módulos (fundo `#1b1b1b`, borda superior vermelha)
  - Nomes com barra vermelha à esquerda (nome em branco 800 e cargo em vermelho)
  - Cards em arco do mesmo tamanho (borda vermelha 3px, raio superior total, nome e cargo embaixo)
  - Cartão de embarque SHA → BRA, painel de voo, "EMBARQUE ABERTO" (bolinha verde), ícones (setas, ✦, avião, código de barras)
- Textos sobre vídeo: sombra leve (`drop-shadow(0 3px 6px rgba(0,0,0,.5)) drop-shadow(0 10px 26px rgba(0,0,0,.35))`).

## Padrões de edição aprovados pelo usuário

- Formato 1080×1920, 30 fps, H.264 (crf 18), AAC 192k, −14 LUFS, pico −1 dBTP.
- Vídeo de iPhone vem em HDR (HLG): converter para SDR com zscale + tonemap hable:
  `zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=saturation=1.08:contrast=1.03`
- Camada gráfica: página HTML 1080×1920 com função `setT(t)` que anima cada elemento por tempo. O Playwright captura cada quadro como PNG transparente e o ffmpeg sobrepõe. Para não cortar o fim, usar como base um `color` de duração fixa.
- **Legenda de fala**: Urbanist 800, 68px, branca com palavras-chave em vermelho, contorno preto **8px** (o usuário pediu mais fino que 12px), centralizada, base em `bottom:440px`, blocos de no máximo 2 linhas com entrada "pop" rápida.
- **Caixas e textos nunca podem cobrir rostos**: medir a posição dos rostos e manter os elementos acima ou abaixo.
- Não colocar foto de uma pessoa que já está em cena (o usuário rejeitou isso).
- Fotos de várias pessoas: sempre do mesmo tamanho (cards em arco iguais, como na arte de referência).
- Boas práticas dos 3 primeiros segundos (aprovadas, "versão B"):
  - cortar o silêncio inicial;
  - punch-in (zoom 1.9→1.0 em ~2,6s, com zoompan sobre 2x);
  - título já visível no quadro 0;
  - carimbo 中国;
  - texto cinético "IMPORTAR / MUDA O JOGO" com caixa vermelha;
  - flash curto e tarja cruzando a tela.
- Fechamento: fundo escuro com brilho vermelho e grade sutil nos 2s finais (no lugar do fim do vídeo bruto).

## Áudio

- Limpeza da voz:
  - noisereduce, com perfil de ruído tirado do silêncio inicial (prop_decrease 0.85);
  - depois `adeclip, highpass=f=85, agate=threshold=0.012:ratio=2.5:range=0.25:attack=8:release=180, deesser=i=0.5, acompressor=threshold=-22dB:ratio=3:attack=5:release=90:makeup=2, alimiter, loudnorm I=-16`.
- Trilha: **composição original sintetizada** (numpy/scipy). Não usar música de terceiros: a rede bloqueia downloads e há risco de direitos autorais.
- Trilha preferida: estilo do reel de referência "CHINA ACADEMY SOLVER ML". É ambiente/cinematográfica, **sem bateria**:
  - Ré maior, ~90–91 BPM;
  - pads e cordas sustentados, grave longo, pulso ou piano abafado em ostinato, coro suave;
  - subida ~12s, impacto ~18s, pausa curta antes do fechamento.
  - A versão v2 usou Si menor → Sol → Ré → Lá; a referência usa Mi menor → Sol → Ré → Lá.
- Volume da trilha: o usuário pediu **mais alta** que 15–20 dB abaixo da voz. Aprovado: **10–13 dB abaixo durante a fala**, ~4 dB nas pausas, com ducking via sidechaincompress (threshold 0.03, ratio 4).

## Ferramentas no ambiente

- ffmpeg estático: `pip install imageio-ffmpeg` e link em `/usr/local/bin/ffmpeg` (tem zscale/tonemap).
- Playwright + Chromium já instalados (`/opt/node22/lib/node_modules/playwright`).
- Transcrição: Hugging Face e openaipublic são bloqueados. Funcionou o pacote npm `sts-whisper-small` com `@huggingface/transformers` (`npm i --ignore-scripts`), `env.allowRemoteModels=false`, `return_timestamps:'word'`.
- Recorte de fundo: `rembg` (modelo isnet-general-use).
- Instagram bloqueado pela rede: o usuário precisa anexar os arquivos.
- **O push para o GitHub dá 403**: entregar os arquivos sempre pelo envio direto e não depender do repositório.

## Próxima tarefa (pedido atual)

Editar um **vídeo de aula do curso** (com o Marcelo; Renan e Felipe aparecem; salas cheias):
- Preencher o vídeo com **elementos animados e chamadas sobre o conteúdo da aula**, no mesmo visual dos elementos acima.
- **Nada de venda**: sem CTA, botão, "vagas limitadas", "garanta sua vaga", preço ou WhatsApp.
- Passos:
  1. Transcrever.
  2. Mapear os momentos (quem fala, aparições do Renan e do Felipe, planos de sala cheia).
  3. Propor um roteiro de chamadas com tempos e mostrar ao usuário.
  4. Mostrar uma prévia de alguns quadros.
  5. Renderizar.
- Ideias de chamadas: título do tema da aula, palavras-chave em destaque, nome e cargo de quem fala (barra vermelha), "AULA AO VIVO"/"NA PRÁTICA", destaques de números e conceitos citados, contador ou marcador dos módulos 01–05 quando forem citados, selo 中国 discreto e legenda de fala.

## Arquivos para anexar na conversa nova

1. O vídeo da aula (arquivo original do celular).
2. `elementos-video.zip` (PNGs transparentes que o usuário já baixou).
3. Opcional: `china-academy_versao-B_final_trilha-referencia-v2.mp4`, como referência do estilo aprovado, e o mp3 "CHINA ACADEMY SOLVER ML" como referência de trilha.
