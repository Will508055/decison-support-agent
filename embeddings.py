import os
from google import genai
from google.genai import types
from chromadb import EmbeddingFunction, Embeddings
from chromadb.utils.embedding_functions import register_embedding_function
from ollama import embeddings


api_key = os.getenv('GOOGLE_API_KEY')
client = genai.Client(api_key=api_key)


@register_embedding_function
class GoogleEmbeddingFunction(EmbeddingFunction):
    def __call__(self, chunk: str) -> Embeddings:
        embeddings = client.models.embed_content(
        model='gemini-embedding-001',
        contents=chunk,
        config=types.EmbedContentConfig(task_type='RETRIEVAL_QUERY')
        )
        return embeddings.embeddings[0].values