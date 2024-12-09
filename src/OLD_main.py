import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import warnings
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from utils import extract_text_from_pdf
from rag import process_text, create_qa_chain

# ========== LOGGING CONFIGURATION ==========
# Only log INFO and ERROR, and suppress warnings and debug logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
warnings.filterwarnings('ignore')

# ========== PATH CONFIGURATION ==========
# Add src folder to Python path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ========== ENVIRONMENT VARIABLES ==========
try:
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        logging.info(f'✅ API Key Loaded: {openai_key[:5]}**********')
    else:
        logging.error('❌ OPENAI_API_KEY not found in .env file or not set')
except Exception as e:
    logging.error(f'❌ Error loading environment variables: {e}')

# ========== FLASK APPLICATION ==========
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

# Global variables to hold the vector store and QA chain
vector_store = None
qa_chain = None

def initialize_rag_system():
    """Load the PDF files from the data folder and create the QA chain."""
    global vector_store, qa_chain
    try:
        logging.info('🔄 Initializing RAG system...')
        data_folder = os.path.join(os.path.dirname(__file__), '../data')
        files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]
        logging.info(f'📂 Files found in data folder: {files}') 

        if not files:
            logging.error('❌ No PDF files found in the data folder. Skipping initialization.')
            return

        file_path = os.path.join(data_folder, files[0])
        logging.info(f'📄 Processing PDF file: {file_path}')

        resume_text = extract_text_from_pdf(file_path)
        if not resume_text:
            logging.error('❌ Failed to extract text from the PDF.')
            return

        logging.info('📄 Text successfully extracted from the PDF')

        vector_store = process_text(resume_text)
        if vector_store is None:
            logging.error('❌ Vector store is None. Check if FAISS was created successfully.')
            return

        logging.info('📚 Text successfully embedded and stored in vector store')

        qa_chain = create_qa_chain(vector_store)
        if qa_chain is not None:
            logging.info('✅ QA chain successfully created with GPT-4-turbo')
        else:
            logging.error('❌ QA chain is None after creation. Check if ChatOpenAI was initialized properly.')

    except Exception as e:
        logging.error(f'❌ Error initializing RAG system: {e}')

@app.route('/')
def index():
    try:
        logging.info('📄 Serving index.html page')
        return render_template('index.html')
    except Exception as e:
        logging.error(f'❌ Error rendering index.html: {e}')
        return f"Error loading page: {e}", 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        question = request.json.get('question')
        logging.info(f'💬 Received question: {question}')
        if not question:
            logging.error('❌ No question received in request')
            return jsonify({"error": "No question received"}), 400
    except Exception as e:
        logging.error(f'❌ Error parsing question from request: {e}')
        return jsonify({"error": "Invalid question format"}), 400

    try:
        if qa_chain is None:
            logging.error('❌ QA chain is not initialized')
            return jsonify({"error": "QA chain is not initialized"}), 500
        
        response = qa_chain.run(question)
        logging.info(f'✅ Response successfully generated: {response}')
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f'❌ Error generating response: {e}')
        return jsonify({"error": "Failed to generate response"}), 500

if __name__ == '__main__':
    logging.info('🚀 Starting Flask app on http://0.0.0.0:5002')
    initialize_rag_system()
    app.run(host="0.0.0.0", port=5002, debug=True)
