import sys
sys.path.append(r'e:/Projetos Faculdade/Fundamentos-IAGenerativa/projeto03')
from retriever import load_conhecimento, build_vector_store, simple_retriever
from llm_client import LLMClient

# set dummy API key to satisfy LLMClient initializer
import os
os.environ['OPENAI_API_KEY'] = 'DUMMY'
os.environ.pop('GROQ_API_KEY', None)

client = LLMClient(provider='openai')  # embeddings calls will fail and fallback to local
knowledge = load_conhecimento()
store = build_vector_store(knowledge, client)
print('chunks:')
for i,item in enumerate(store,1):
    print(i, item['text'][:80].replace('\n',' '))

# helper to show top similarities
from retriever import cosine_similarity

def debug_query(q):
    print("\n=== QUERY ->", q)
    try:
        q_emb = client.get_embedding(q)
    except Exception as e:
        print("error embedding", e)
        return
    sims = [(item['text'], cosine_similarity(q_emb, item['vector'])) for item in store]
    sims.sort(key=lambda x: x[1], reverse=True)
    for text,score in sims[:3]:
        print(score, text[:60].replace('\n',' '))
    print("retriever output:", simple_retriever(q, store, client))

queries=["quero saber o email de suporte","formas de reembolso","qual o prazo para arrependimento","que dia é hoje"]
for q in queries:
    debug_query(q)
