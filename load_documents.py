from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
import tempfile
import os

def text_loader(file) -> TextLoader:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
        tmp_file.write(file.getvalue())
        tmp_path = tmp_file.name
    return TextLoader(tmp_path)

def pdf_loader(file) -> PyPDFLoader:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(file.getvalue())
        tmp_path = tmp_file.name
    return PyPDFLoader(tmp_path)

def select_loader(file, file_type):
    if file_type == "PDF":
        loader = pdf_loader(file)
    elif file_type == "Text File":
        loader = text_loader(file)
    return loader