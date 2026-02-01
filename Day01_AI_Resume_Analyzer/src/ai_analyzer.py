from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def analyze_similarity(resume_text: str, job_text: str) -> float:
    embeddings = MODEL.encode([resume_text, job_text])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
    return round(similarity[0][0] * 100, 2)
