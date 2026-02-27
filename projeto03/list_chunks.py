import os, sys, re
sys.path.append(r'e:/Projetos Faculdade/Fundamentos-IAGenerativa/projeto03')
from retriever import load_conhecimento, build_vector_store
from llm_client import LLMClient
os.environ['OPENAI_API_KEY']='DUMMY'
client=LLMClient(provider='openai')
kn=load_conhecimento()
store=build_vector_store(kn, client)
print('chunks total', len(store))
for i,item in enumerate(store,1):
    t=item['text']
    has_email = '@' in t
    has_phone = bool(re.search(r"\(\d{2}\)\s*\d{4,5}-\d{4}", t))
    lower=t.lower()
    print('---',i,'has_email=',has_email,'has_phone=',has_phone,'has_contato=',('contato' in lower or 'suporte' in lower))
    print(t)
    print()
