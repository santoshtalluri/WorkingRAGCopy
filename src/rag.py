import logging
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_text(text):
    """Process and split text into vector embeddings."""
    try:
        chunks = RecursiveCharacterTextSplitter(chunk_size=500).split_text(text)
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        logging.error(f'❌ Error processing text: {e}')
        return None

def create_qa_chain(vector_store):
    """Create a QA chain from the vector store."""
    try:
        if vector_store is None:
            logging.error('❌ Vector store is None. Cannot create QA chain.')
            return None
        llm = ChatOpenAI(model="gpt-4-turbo")
        retriever = vector_store.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        return qa_chain
    except Exception as e:
        logging.error(f'❌ Error creating QA chain: {e}')
        return None

def check_if_resume(text):
    """Check if the document is a resume based on simple keywords."""
    resume_keywords = ['education', 'experience', 'skills', 'projects']
    return any(keyword in text.lower() for keyword in resume_keywords)
