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
    """Retorna o trecho mais similar ao `query` usando embeddings.

    Se nada for encontrado com score positivo, devolve mensagem de fallback.
    """
    if not store:
        # nenhum documento carregado -> contexto ausente
        return ""  # sinalizar para quem chamou que não há contexto
    try:
        q_emb = client.get_embedding(query)
    except Exception as e:
        print(f"Erro ao gerar embedding de consulta: {e}")
        return ""
    sims = [(item["text"], cosine_similarity(q_emb, item["vector"])) for item in store]
    sims.sort(key=lambda x: x[1], reverse=True)
    if sims and sims[0][1] > 0:
        return sims[0][0]
    return ""  # nada relevante encontrado
