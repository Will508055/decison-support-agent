import doc_parsing as dp
import chromadb
from chromadb.utils import embedding_functions
import embeddings


docs = dp.list_documentation_files()
client = chromadb.PersistentClient(path='chroma_data')

collection = client.get_or_create_collection(
    name='motorcycle_cornering_docs',
    embedding_function=embeddings.GoogleEmbeddingFunction()
    )

def is_new_document(text: str) -> bool:
    results = collection.query(
        query_texts=[text],
        n_results=1
    )

    return len(results['ids'][0]) == 0

## TODO: Add documents to collection if they are new
# check if doc is new based on title which can be retrieved immediately
# if new, parse the document to get the text and then embed and add to collection
# only parse if they are new to avoid unnecessary parsing time