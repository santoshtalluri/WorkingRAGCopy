import logging
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS  # This import is still valid
from langchain_community.chat_models import ChatOpenAI  # No change required
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure logging to show only INFO and ERROR (suppress DEBUG)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== FUNCTION TO PROCESS TEXT ==========
def process_text(text):
    """Splits and embeds the text into a vector store."""
    try:
        logging.info('🔄 Starting to split text into chunks...')
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(text)
        logging.info(f'✅ Text successfully split into {len(chunks)} chunks')
    except Exception as e:
        logging.error(f'❌ Error splitting text into chunks: {e}')
        raise e

    try:
        logging.info('🔄 Generating embeddings for the chunks using OpenAIEmbeddings...')
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")  # Updated instantiation
        vector_store = FAISS.from_texts(chunks, embedding=embeddings)
        logging.info('✅ Successfully created FAISS vector store with embeddings')
    except Exception as e:
        logging.error(f'❌ Error generating embeddings or creating FAISS vector store: {e}')
        raise e

    return vector_store

# ========== FUNCTION TO CREATE QA CHAIN ==========
def create_qa_chain(vector_store):
    """Create the QA chain using ChatGPT."""
    try:
        logging.info('🔄 Creating QA chain using GPT-4-turbo...')
        llm = ChatOpenAI(temperature=0, model="gpt-4-turbo")

        if vector_store is None:
            logging.error('❌ Vector store is None. Cannot create QA chain.')
            return None

        retriever = vector_store.as_retriever()
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )

        if qa_chain is not None:
            logging.info('✅ QA chain successfully created with GPT-4-turbo')
        else:
            logging.error('❌ QA chain is None. Check if ChatOpenAI was initialized properly.')
    except Exception as e:
        logging.error(f'❌ Error creating QA chain: {e}')
        raise e

    return qa_chain
