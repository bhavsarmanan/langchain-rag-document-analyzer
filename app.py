import streamlit as st
from load_models import load_models
#from load_documents import text_loader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_ollama import ChatOllama


from langchain import hub
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
#from langchain_community.hub import pull as hub_pull

#defined functions
from ingest_main import ingest_in_faiss
from create_template import custom_template
from design_page import draw_sidebar
from invoke_main import invoke_llm



def format_docs(documents):
    return "\n\n".join(documents.page_content for documents in documents)



st.title("Document Analyzer")
output=""

models = load_models()
loader = draw_sidebar()

if loader is not None:
    document = loader.load()


    print("Splitting text...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30,separator="\n")
    texts = text_splitter.split_documents(document)
    #st.write(texts)

    print("Embedding text...")
    embeddings = OllamaEmbeddings(model="llama3.2")
  

    
    # Get embeddings for each chunk of text
    #embedded_texts = [embeddings.embed_query(text.page_content) for text in texts]
    print("Ingesting context...")
    vectorstore = ingest_in_faiss(texts, embeddings)

    print("Initiate prompt template...")
    retrival_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    retrival_qa_chat_history_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    #custom_rag_prompt = custom_template()
    #docsearch = FAISS(embedding_function=embeddings,index_name="rag_index",docstore=InMemoryDocstore({}))

    #custom_rag_prompt = PromptTemplate.from_template(custom_template)
    template = """ answer the quesition with just 1 or 2 sentences max.

            Also your name is Siri

    {context}

    question: {question}    

    answer:"""

    custom_rag_prompt = PromptTemplate.from_template(template)

#draw_sidebar()

    selected_model = st.radio(":blue[Select the model]", options=models,horizontal=True )
    #st.write(models)
    llm = ChatOllama(model=selected_model)
    #alternate implmentation which is currently commented
    #rag_chain = (
    #                {"context": vectorstore.as_retriever() | format_docs,"question":RunnablePassthrough()}
    #                | custom_rag_prompt
    #                | llm 
    #            )
   
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Response powered by " + selected_model ):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        #alternate way of invokding chain which is currently commented
        #res = rag_chain.invoke(prompt)
        #res = invoke_llm(llm,vectorstore,prompt,retrival_qa_chat_prompt,st.session_state.message)
        res=invoke_llm(llm,vectorstore,prompt,retrival_qa_chat_history_prompt,st.session_state)
        #st.write(res)
                

        
        # Display assistant response in chat message container
        with st.chat_message("ai"):
            #output = res['answer']
            output = res['answer'] + "\n\n" +':blue[response powered by ' + selected_model +']'
            st.markdown(output)
            
        st.session_state.messages.append({"role": "assistant", "content": output})

    # Add assistant response to chat history
