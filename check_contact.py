import re
p = r'e:/Projetos Faculdade/Fundamentos-IAGenerativa/projeto03/conhecimento/conhecimento.txt'
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
print('email present?', bool(re.search(r"[\w\.-]+@[\w\.-]+", s)))
print('phone present?', bool(re.search(r"\(\d{2}\)\s*\d{4,5}-\d{4}", s)))
m = re.search(r"\(\d{2}\)\s*\d{4,5}-\d{4}", s)
print('phone match:', m.group(0) if m else None)
