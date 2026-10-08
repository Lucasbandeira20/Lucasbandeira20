"""Salva em arquivo o resultado de uma leitura do Google Sheets já feita nesta conversa.

As ferramentas do Sheets devolvem o resultado só para o chat. Este script procura, no
histórico da sessão (~/.claude/projects/*/*.jsonl), o resultado mais recente cujo texto
contém o trecho informado (normalmente o range, ex.: "BASE PRODUTOS TIKTOK'!G1:G2000")
e grava o JSON em disco. Se o resultado foi grande e o próprio app já salvou em arquivo,
copia esse arquivo.

Uso: python3 salvar_resultado.py "<trecho do range>" saida.json
"""
import glob
import json
import os
import re
import shutil
import sys

trecho, saida = sys.argv[1], sys.argv[2]
arqs = sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime)
achado = None
for line in open(arqs[-1], encoding='utf-8'):
    if '"tool_result"' not in line:
        continue
    d = json.loads(line)
    for c in d.get('message', {}).get('content', []):
        if not isinstance(c, dict) or c.get('type') != 'tool_result':
            continue
        cc = c.get('content')
        txt = cc if isinstance(cc, str) else ''.join(x.get('text', '') for x in cc if isinstance(x, dict))
        if trecho.replace("'", "") in txt.replace("'", ""):
            achado = txt
if achado is None:
    sys.exit(f'Nenhum resultado com "{trecho}" encontrado.')
m = re.search(r'saved to:? (\S+\.txt)', achado)
if m and os.path.exists(m.group(1)):
    shutil.copy(m.group(1), saida)
else:
    i = achado.find('{')
    obj, _ = json.JSONDecoder().raw_decode(achado[i:])
    json.dump(obj, open(saida, 'w'), ensure_ascii=False)
d = json.load(open(saida))
n = len(d.get('values', d.get('sheets', []))) if isinstance(d, dict) else len(d)
print(f'salvo {saida} ({n} linhas/blocos)')
