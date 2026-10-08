"""Funções comuns: texto, números pt-BR, taxas do TikTok, preços redondos e busca por nome."""
import difflib
import json
import re
import unicodedata


def norm(s):
    s = unicodedata.normalize('NFKD', str(s).lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def num(s):
    """'R$ 1.234,56' / '22,02%' / 1234.5 -> float (None se vazio)."""
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).replace('R$', '').replace('%', '').strip().replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def g(r, i):
    return r[i] if len(r) > i else ''


def load_values(path):
    """Lê um JSON salvo de get_values ({'values': [...]}) ou uma lista pura."""
    d = json.load(open(path))
    return d['values'] if isinstance(d, dict) else d


# ---------- TikTok ----------
def ttm(c, p):
    """Margem TikTok: comissão (<50: 10%+4; >=50: 6%+6) + frete 6% (teto 50) + imposto 7,3%."""
    f = (p * 0.1 + 4 if p < 50 else p * 0.06 + 6) + min(p * 0.06, 50)
    return 1 - (c + f + p * 0.073) / p


NICE = sorted(set([n + 0.90 for n in range(4, 50)] +
                  [k * 10 - d for k in range(5, 3000) for d in (0.01, 0.10, 1.10, 2.10, 4.50, 5.10)]))
NICE = [round(x, 2) for x in NICE if x > 4]


def first_m(c, alvo):
    """Primeiro preço redondo com margem >= alvo."""
    return next(v for v in NICE if ttm(c, v) >= alvo)


def nice_below(x):
    """Maior preço redondo estritamente menor que x."""
    c = [y for y in NICE if y < x - 1e-9]
    return c[-1] if c else None


# ---------- busca por nome ----------
FILLER = {'mesa', 's', 'coroa', 'original', 'preto', 'new', 'com', 'na', 'caixa', 'true', 'cor', 'marrom',
          'marro', 'de', 'p', 'fx', 'absolute', 'cassete', 'moto', 'carro'}


def base_name(name):
    b = re.split(r'\s*(?:Cor|Tamanho[^:;]*|Voltagem)\s*:', str(name))[0]
    b = re.sub(r'\s+Cod\d+\s*$', '', b)
    return norm(b)


def toks(x):
    return re.sub(r'([a-z])(\d)', r'\1 \2', re.sub(r'(\d)([a-z])', r'\1 \2', x)).split()


def same_product(a, b):
    ta, tb = toks(a), toks(b)
    na = sorted(t for t in ta if any(ch.isdigit() for ch in t))
    nb = sorted(t for t in tb if any(ch.isdigit() for ch in t))
    if na != nb:
        return False
    return (set(ta) ^ set(tb)) <= FILLER


class Index:
    """Índice nome -> valor, com busca exata, pelo nome-base (sem 'Cor:'/'Tamanho:') e aproximada."""

    def __init__(self):
        self.exact, self.base = {}, {}

    def add(self, raw_name, value):
        self.exact.setdefault(norm(raw_name), value)
        self.base.setdefault(base_name(raw_name), value)

    def find(self, name):
        n = norm(name)
        if n in self.exact:
            return self.exact[n], 'exato'
        b = base_name(name)
        if b in self.base:
            return self.base[b], 'base'
        if b in self.exact:
            return self.exact[b], 'base'
        for cand in difflib.get_close_matches(b, list(self.base), 5, 0.85):
            if same_product(b, cand):
                return self.base[cand], 'aprox'
        return None, None
