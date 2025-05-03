from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

def invoke_llm(llm,vectorstore,prompt,retrival_qa_chat_prompt):
    stuff_document_chain = create_stuff_documents_chain(llm,retrival_qa_chat_prompt)
    qa = create_retrieval_chain(retriever=vectorstore.as_retriever(),combine_docs_chain=stuff_document_chain)
    response = qa.invoke(input={'input':prompt})
    return response

