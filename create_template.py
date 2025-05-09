from langchain.prompts import PromptTemplate
def custom_template():
    template = """ answer the quesition with just 1 or 2 sentences max.

    Also your name is Documento

    {context}

    question: {question}    

    answer:
    """
    return PromptTemplate.from_template(template)