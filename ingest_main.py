from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from uuid import uuid4
import faiss


def ingest_in_faiss(texts, embeddings):

    #print(texts)

    index = faiss.IndexFlatL2(len(embeddings.embed_query("Hello World")))
    vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
    )

    uuids = [str(uuid4()) for _ in range(len(texts))]

    #vector_store.add_documents(documents=texts, ids=uuids)
    vector_store.from_documents(documents=texts,embedding=embeddings)
    
    vectorstore = FAISS.from_documents(documents=texts,embedding=embeddings)
    #vectorstore = FAISS.add_documents(documents=texts,ids=uuids,embedding=embeddings)
    return vectorstore

def ingest_in_pgvector():
    pass


