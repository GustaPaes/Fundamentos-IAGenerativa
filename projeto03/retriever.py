# RAG Simplificado com embeddings
import os
from typing import List, Dict

from llm_client import LLMClient


def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _read_pdf(path: str) -> str:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError("PyPDF2 não está instalado, instale via requirements.txt")
    reader = PdfReader(path)
    pages = [p.extract_text() or "" for p in reader.pages]
    return "\n".join(pages)


def _read_docx(path: str) -> str:
    try:
        import docx
    except ImportError:
        raise ImportError("python-docx não está instalado, instale via requirements.txt")
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)


def load_conhecimento() -> str:
    """Lê todo o conteúdo textual dos arquivos presentes na pasta de conhecimento.

    Suporta .txt, .pdf e .docx. Qualquer arquivo não reconhecido será ignorado.
    O texto de cada arquivo é concatenado com duas quebras de linha para separar.

    A pasta é localizada em relação a este módulo, garantindo que o
    script possa ser executado de qualquer diretório de trabalho.
    """
    base_dir = os.path.dirname(__file__)
    base = os.path.join(base_dir, "conhecimento")
    pieces: List[str] = []
    if not os.path.isdir(base):
        raise FileNotFoundError(f"Diretório de conhecimento não encontrado: {base}")

    for fname in os.listdir(base):
        path = os.path.join(base, fname)
        if not os.path.isfile(path):
            continue
        lower = fname.lower()
        try:
            if lower.endswith(".txt"):
                pieces.append(_read_txt(path))
            elif lower.endswith(".pdf"):
                pieces.append(_read_pdf(path))
            elif lower.endswith(".docx"):
                pieces.append(_read_docx(path))
            else:
                # ignora outros tipos
                continue
        except Exception as e:
            print(f"Erro ao ler {fname}: {e}")
    return "\n\n".join(pieces)


def cosine_similarity(a: List[float], b: List[float]) -> float:
    # cálculo manual para evitar dependências extras
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def build_vector_store(conhecimento: str, client: LLMClient) -> List[Dict]:
    """Constrói uma lista de chunks com seus embeddings.

    Divide o conhecimento em seções menores para melhor recuperação.
    """
    # dividir por seções (------ ou \n\n)
    chunks = []
    
    # primeiro, dividir por seções principais (com ----)
    sections = conhecimento.split("--------------------------------------------------")
    for section in sections:
        # depois, dividir cada seção por parágrafos vazios
        paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]
        chunks.extend(paragraphs)
    
    # remover chunks muito pequenos (menos de 20 caracteres)
    chunks = [c for c in chunks if len(c) > 20]
    
    store: List[Dict] = []
    for i, chunk in enumerate(chunks):
        try:
            emb = client.get_embedding(chunk)
            store.append({"text": chunk, "vector": emb})
        except Exception as e:
            # registra erro mas continua com próximo trecho
            print(f"Aviso: falha ao indexar trecho {i+1}: {e}")
    return store


def simple_retriever(query: str, store: List[Dict], client: LLMClient) -> str:
    """Retorna o trecho mais similar ao `query` usando busca híbrida.

    Tenta embeddings primeiro, depois busca léxica por palavras-chave.
    """
    if not store:
        return ""
    
    import re
    
    # prepare lexical information early
    query_lower = query.lower()
    wants_email = 'email' in query_lower or 'e-mail' in query_lower

    # if the user is asking for an email address, return the first chunk that
    # contains an at-sign or the word 'suporte'. doing this before embeddings
    # avoids incorrect matches for vague queries like "quero saber o email".
    if wants_email:
        for item in store:
            text_lower = item["text"].lower()
            if '@' in text_lower or 'suporte' in text_lower:
                return item["text"]

    # 1. Busca vetorial (embeddings)
    try:
        q_emb = client.get_embedding(query)
    except Exception as e:
        print(f"Erro ao gerar embedding de consulta: {e}")
        return ""

    sims = [(item["text"], cosine_similarity(q_emb, item["vector"])) for item in store]
    sims.sort(key=lambda x: x[1], reverse=True)

    # if the top similarity is sufficiently high, trust embedding result
    # raising threshold reduces chance of returning unrelated chunks
    if sims:
        top_sim = sims[0][1]
        if top_sim > 0.30:
            return sims[0][0]
    
    # 2. Busca léxica (palavras-chave)
    query_lower = query.lower()
    query_words = set(re.findall(r'\b[a-záéíóúâêôãõç]+\b', query_lower))
    stopwords = {'o', 'a', 'de', 'da', 'do', 'é', 'para', 'em', 'ou', 'e', 'um', 'uma', 'que', 'por', 'qual', 'como'}
    query_words = query_words - stopwords
    
    # special handling for email queries
    wants_email = 'email' in query_lower or 'e-mail' in query_lower
    
    if not query_words and not wants_email:
        # no lexical clues at all, treat as unknown and skip embedding result
        return ""
    
    best_score = 0
    best_text = ""
    for item in store:
        text_lower = item["text"].lower()
        # email logic: if query asks for email and text contains '@' or 'suporte' word, pick it
        if wants_email and ('@' in text_lower or 'suporte' in text_lower):
            return item["text"]
        text_words = set(re.findall(r'\b[a-záéíóúâêôãõç]+\b', text_lower))
        matches = len(query_words & text_words)
        if matches > best_score:
            best_score = matches
            best_text = item["text"]
    
    return best_text if best_score > 0 else ""


def find_contact_chunk(store: List[Dict]) -> str:
    """Procura no store por um trecho que contenha e-mail ou telefone.

    Retorna o texto do primeiro chunk que contém '@' ou um padrão de
    telefone comum. Retorna string vazia se não encontrar.
    """
    import re
    phone_re = re.compile(r"\(\d{2}\)\s*\d{4,5}-\d{4}")
    # first pass: prefer chunks that actually contain an email or phone
    for item in store:
        text = item.get("text", "")
        if "@" in text:
            return text
        if phone_re.search(text):
            return text

    # second pass: fallback to chunks that mention contato/suporte/telefone
    for item in store:
        text = item.get("text", "")
        lower = text.lower()
        if "contato" in lower or "suporte" in lower or "telefone" in lower:
            return text
    return ""
