import os, sys, re
sys.path.append(r'e:/Projetos Faculdade/Fundamentos-IAGenerativa/projeto03')
from retriever import load_conhecimento, build_vector_store, find_contact_chunk
from llm_client import LLMClient
os.environ['OPENAI_API_KEY']='DUMMY'
client=LLMClient(provider='openai')
kn=load_conhecimento()
store=build_vector_store(kn, client)
fc = find_contact_chunk(store)
print('find_contact_chunk returned snippet:\n', (fc or '(none)')[:400])
# find index
for i,item in enumerate(store,1):
    if item['text'] == fc:
        print('match index', i)
        break
else:
    print('no exact match found')
PY
