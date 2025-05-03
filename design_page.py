import streamlit as st
from load_documents import select_loader

def draw_sidebar():
    st.sidebar.title("Upload document to be analyzed")
    selection = st.sidebar.selectbox("Documents that you can upload", ["PDF", "Text File"])

    if st.sidebar.button("Clear chat history"):
        st.session_state.messages = []

    if selection == "PDF":
        file = st.sidebar.file_uploader("Upload a file", type=["pdf"])
    elif selection == "Text File":
        file = st.sidebar.file_uploader("Upload a file", type=["txt"])

    if file is not None:
        loader = select_loader(file, selection)
        return loader
    else:
        st.sidebar.error("Please upload a file")



    