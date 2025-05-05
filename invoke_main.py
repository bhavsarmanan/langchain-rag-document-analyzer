from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
import streamlit as st

def invoke_llm(llm,vectorstore,prompt,retrival_qa_chat_prompt,chat_history):
    if "message" not in chat_history:
        chat_history.messages = []

    stuff_document_chain = create_stuff_documents_chain(llm,retrival_qa_chat_prompt)
    history_aware_retrieval = create_history_aware_retriever(llm=llm,retriever=vectorstore.as_retriever(),prompt=retrival_qa_chat_prompt)
    #qa = create_retrieval_chain(retriever=vectorstore.as_retriever(),combine_docs_chain=stuff_document_chain)
    qa=create_retrieval_chain(retriever=history_aware_retrieval,combine_docs_chain=stuff_document_chain)
    response = qa.invoke(input={'input':prompt,'chat_history':chat_history})
    return response

