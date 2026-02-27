import os, sys
sys.path.append(r'e:/Projetos Faculdade/Fundamentos-IAGenerativa/projeto03')
from retriever import load_conhecimento, build_vector_store, simple_retriever
from llm_client import LLMClient
# garantir que o cliente seja inicializável sem chave real
os.environ['OPENAI_API_KEY'] = 'DUMMY'
client = LLMClient(provider='openai')
knowledge = load_conhecimento()
store = build_vector_store(knowledge, client)
q = 'quero saber o email de suporte'
contexto = simple_retriever(q, store, client)
print('--- contexto ---')
print(contexto)
import re
email = re.search(r'[\w\.-]+@[\w\.-]+', contexto)
phone = re.search(r'\(\d{2}\)\s*\d{4,5}-\d{4}', contexto)
hours = re.search(r'segunda a sexta-feira[^,\.]*|de segunda a sexta[^,\.]*', contexto, re.IGNORECASE)
parts = []
if email: parts.append('e-mail: '+email.group(0))
if phone: parts.append('telefone: '+phone.group(0))
if hours: parts.append('horário: '+hours.group(0).strip())
if parts:
    print('\nstandardized: ' + 'Você pode entrar em contato conosco por ' + ' ou '.join(parts) + '.')
else:
    print('\nno contact found')
