import os
from google import genai
from google.genai import types
from chromadb import EmbeddingFunction, Embeddings
from chromadb.utils.embedding_functions import register_embedding_function


api_key = os.getenv('GOOGLE_API_KEY')
client = genai.Client(api_key=api_key)


@register_embedding_function
class GoogleEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model='gemini-embedding-001'):
        self.model = model
    
    def __call__(self, docs: list[str]) -> Embeddings:
        embeddings = client.models.embed_content(
            model=self.model,
            contents=docs,
            config=types.EmbedContentConfig(task_type='RETRIEVAL_QUERY')
        )
        embeddings_list = [embedding.values for embedding in embeddings.embeddings]
        return embeddings_list