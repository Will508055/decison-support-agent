from . import doc_parsing as dp
import chromadb
from chromadb.utils import embedding_functions
from . import embeddings
from . import prompts


client = chromadb.PersistentClient(path='chroma_data')

collection = client.get_or_create_collection(
    name='motorcycle_cornering_docs',
    embedding_function=embeddings.GoogleEmbeddingFunction()
    )


def is_new_document(file_name: str) -> bool:
    existing_ids = collection.get()['ids']
    title = file_name.split('.')[0]
    return not any(doc_id.startswith(title) for doc_id in existing_ids)


def update_vector_db():
    new_docs = [file for file in dp.list_documentation_files() if is_new_document(file.split('\\')[-1])]
    if len(new_docs) > 0:
        print(f'Documentation files to add: {[doc.split("\\")[-1] for doc in new_docs]}')
    docs_to_add = {}
    
    for doc in new_docs:
        title = doc.split('\\')[-1].split('.')[0]
        text = dp.parse_document(doc)
        if text is None:
            print(f'Skipping {title} due to parsing issues.')
            continue
        docs_to_add[title] = text
    
    for title, text in docs_to_add.items():
        chunks = dp.chunk_text(text)
        for i, chunk in enumerate(chunks):
            collection.add(
                ids=f'{title}_chunk_{i}',
                documents=chunk
            )
        print(f'Added {title} to vector database.')
    print('Vector database up-to-date.')
    return None


def query_vector_db(conditions: prompts.ConditionsResponse, scene: prompts.SceneResponse, n_results: int = 5) -> str:
    query = prompts.db_query(conditions, scene)
    results = collection.query(query_texts=[query], n_results=n_results)
    return ' '.join(results['documents'][0])