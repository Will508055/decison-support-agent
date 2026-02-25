import doc_parsing as dp
import chromadb
from chromadb.utils import embedding_functions
import embeddings


client = chromadb.PersistentClient(path='chroma_data')

collection = client.get_or_create_collection(
    name='motorcycle_cornering_docs',
    embedding_function=embeddings.GoogleEmbeddingFunction()
    )


def is_new_document(title: str) -> bool:
    results = collection.get(
        ids=[title]
    )
    
    return len(results['ids']) == 0


def update_vector_db():
    new_docs = [file for file in dp.list_documentation_files() if is_new_document(file.split('\\')[-1])]
    titles = [doc.split('\\')[-1] for doc in new_docs]
    texts = dp.parse_documentation(new_docs)
    try:
        for i in range(len(titles)): ### implement chunking logic
            collection.add(
                ids=titles[i],
                documents=texts[i]
            )
    except Exception as e:
        print(f'Error adding documents to vector database: {e}')
    print('Vector database up-to-date.')
    return None