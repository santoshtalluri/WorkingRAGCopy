import os
import sys
import logging
import requests
import cloudscraper
import json

from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Import RAG and formatting functions
from rag import process_text, create_qa_chain
from utils.utils import extract_text_from_pdf, load_json_keywords
from utils.formatter import format_job_details # Importing from the formatter.py file

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure 'src' is part of the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
try:
    load_dotenv(override=True)
    logging.info('✅ Environment variables loaded successfully.')
except Exception as e:
    logging.error(f'❌ Error loading environment variables: {e}')

# Set up Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# 🔥 Serve files from the data folder statically
data_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
app.config['DATA_FOLDER'] = data_folder_path

# Global variables
vector_store = None
qa_chain = None
files_used_in_training = []  # Tracks files used for training


def initialize_rag_system():
    """Load and process PDF files from the data folder."""
    global vector_store, qa_chain, files_used_in_training
    try:
        data_folder = os.path.join(os.path.dirname(__file__), '../data')
        pdf_files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]

        if not pdf_files:
            logging.error('❌ No PDF files in the data folder. Please upload a file to continue.')
            return

        files_used_in_training = pdf_files  # Update list of files used for RAG training

        all_text = ''.join([extract_text_from_pdf(os.path.join(data_folder, f)) for f in pdf_files])
        vector_store = process_text(all_text)
        
        qa_chain = create_qa_chain(vector_store)
    except Exception as e:
        logging.error(f'❌ Error initializing RAG system: {e}')


@app.route('/')
def index():
    """Serve the main HTML page."""
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f'❌ Error rendering index.html: {e}')
        return f"Error loading page: {e}", 500


@app.route('/analyze-job', methods=['POST'])
def analyze_job_url():
    """Handles job URL input and extracts job details from the page."""
    try:
        data = request.get_json()
        url = data.get('url')

        if not url or not url.startswith(('http://', 'https://')):
            logging.error('❌ Invalid URL format.')
            return jsonify({"message": "URL format expected as input", "success": False}), 400

        logging.info(f'🌐 Received URL for analysis: {url}')

        # Use cloudscraper to bypass Cloudflare
        try:
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url, timeout=10)
            if response.status_code != 200:
                raise Exception(f"Status code {response.status_code}")
        except Exception as e:
            logging.error(f'❌ Error accessing URL using cloudscraper: {e}')
            return jsonify({"message": "Could not access the URL or it took too long to respond.", "success": False}), 400

        # Parse the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract job details
        job_details = extract_job_details(soup)

        if not job_details or not job_details.get('job_description') or not job_details.get('job_title'):
            logging.error('❌ The provided URL does not contain a job posting.')
            return jsonify({"message": "Provided URL does not contain a job, please verify", "success": False}), 400

        logging.info(f'✅ Successfully extracted job details for URL: {url}')
        return jsonify({"message": "Job URL validated successfully!", "success": True, "job_details": job_details})

    except Exception as e:
        logging.error(f'❌ Error analyzing URL: {e}', exc_info=True)
        return jsonify({"message": "An error occurred during URL analysis", "success": False}), 500


def extract_clean_text(text):
    """Remove HTML tags and unnecessary whitespace from text."""
    try:
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        logging.error(f'❌ Error cleaning text: {e}')
        return 'Not available'


def extract_section_text(soup, section_key, job_keywords):
    """
    Extracts a specific section from the page using the provided job keywords.
    
    Args:
        soup (BeautifulSoup): The parsed HTML content of the job page.
        section_key (str): The key for which the section is being extracted (e.g., 'job_description', 'required_skills').
        job_keywords (dict): A dictionary of job section headers loaded from job_keywords.json.
    
    Returns:
        str: The extracted and cleaned text for the section or 'Not available' if not found.
    """
    try:
        section_headers = job_keywords.get(section_key, [])
        
        for header in section_headers:
            section = soup.find(string=lambda text: text and header.lower() in text.lower())
            if section:
                # Extract the parent tag containing the section
                parent_tag = section.find_parent()
                if parent_tag:
                    text_content = parent_tag.get_text(separator=' ', strip=True)
                    # Clean the text to remove extra whitespace and line breaks
                    cleaned_text = re.sub(r'\s+', ' ', text_content)
                    logging.info(f'✅ Extracted {section_key} successfully from header "{header}"')
                    return cleaned_text
        
        logging.warning(f'⚠️ Could not extract section {section_key} from the page.')
        return 'Not available'
    
    except Exception as e:
        logging.error(f'❌ Error extracting section {section_key}: {e}', exc_info=True)
        return 'Not available'

def extract_job_details(soup):
    """Extract job details like title, skills, description, company, and location."""
    try:
        logging.info('🕵️ Extracting job details from the HTML content...')
        
        job_details = {}

        # Extract from JSON-LD (if exists)
        try:
            json_ld_data = soup.find('script', {'type': 'application/ld+json'})
            if json_ld_data:
                structured_data = json.loads(json_ld_data.string)
                if isinstance(structured_data, dict) and 'JobPosting' in str(structured_data):
                    for item in structured_data.get('@graph', []):
                        if item.get('@type') == 'JobPosting':
                            job_details['job_title'] = item.get('title', 'Not available')
                            job_details['job_description'] = item.get('description', 'Not available')
                            job_details['location'] = item.get('jobLocation', {}).get('address', {}).get('addressLocality', 'Not available')
                            job_details['company_name'] = item.get('hiringOrganization', {}).get('name', 'Not available')
                            job_details['pay_range'] = item.get('baseSalary', 'Not available')
                            break
        except Exception as e:
            logging.error(f'⚠️ Unable to extract JSON-LD content: {e}')

        # Extract from meta tags (fallback if JSON-LD fails)
        try:
            job_details['company_name'] = soup.find('meta', {'property': 'og:site_name'})['content'] if soup.find('meta', {'property': 'og:site_name'}) else 'Not available'
            job_details['job_title'] = soup.find('meta', {'property': 'og:title'})['content'] if soup.find('meta', {'property': 'og:title'}) else 'Not available'
            job_details['job_description'] = soup.find('meta', {'property': 'og:description'})['content'] if soup.find('meta', {'property': 'og:description'}) else 'Not available'
        except Exception as e:
            logging.error(f'⚠️ Unable to extract meta tag details: {e}')

        # Extract directly from page content
        try:
            if 'job_title' not in job_details or job_details['job_title'] == 'Not available':
                title_tag = soup.find('h1', class_='job-title') or soup.find('h1')
                job_details['job_title'] = title_tag.get_text(strip=True) if title_tag else 'Not available'

            if 'job_description' not in job_details or job_details['job_description'] == 'Not available':
                desc_tag = soup.find('div', class_='job-description') or soup.find('section', class_='description') or soup.find('div', id='job-description')
                job_details['job_description'] = desc_tag.get_text(strip=True) if desc_tag else 'Not available'

            if 'location' not in job_details or job_details['location'] == 'Not available':
                location_tag = soup.find('span', class_='job-location') or soup.find('span', itemprop='addressLocality')
                job_details['location'] = location_tag.get_text(strip=True) if location_tag else 'Not available'

            if 'company_name' not in job_details or job_details['company_name'] == 'Not available':
                company_tag = soup.find('div', class_='company-name') or soup.find('span', itemprop='name')
                job_details['company_name'] = company_tag.get_text(strip=True) if company_tag else 'Not available'
        except Exception as e:
            logging.error(f'⚠️ Error extracting from HTML content: {e}', exc_info=True)

        formatted_job_details = {k: v.replace('\n', ' ').strip() if isinstance(v, str) else v for k, v in job_details.items()}
        
        logging.info(f'✅ Successfully extracted job details: {formatted_job_details}')
        return formatted_job_details

    except Exception as e:
        logging.error(f'❌ Error extracting job details: {e}', exc_info=True)
        return {}


def extract_company_name(soup):
    """Try to extract the company name from meta tags or known patterns."""
    try:
        company_name = soup.find('meta', {'property': 'og:site_name'})
        if company_name:
            return company_name.get('content', 'Not available')

        title = soup.title.string if soup.title else ''
        company_match = [word for word in title.split() if word.lower() in ['google', 'microsoft', 'amazon']]
        if company_match:
            return company_match[0]

        return 'Not available'
    except Exception as e:
        logging.error(f'❌ Error extracting company name: {e}')
        return 'Not available'

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
    app.run(host="0.0.0.0", port=5002, debug=False)

@app.errorhandler(404)
def page_not_found(e):
    """Log and handle missing routes."""
    logging.error(f"❌ Route not found: {request.url}")
    return jsonify({"error": "The requested URL was not found on the server."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    """Log and handle unsupported HTTP methods."""
    logging.error(f"❌ Method not allowed: {request.method} on {request.url}")
    return jsonify({"error": "The method is not allowed for the requested URL."}), 405

@app.errorhandler(Exception)
def handle_exception(e):
    """Log and handle all unhandled exceptions."""
    logging.error(
        f"❌ An unexpected error occurred: {e}\n"
        f"Request Data: Method={request.method}, URL={request.url}, Headers={dict(request.headers)}, Body={request.get_data(as_text=True)}",
        exc_info=True
    )
    return jsonify({"error": "An internal server error occurred."}), 500


if __name__ == '__main__':
    initialize_rag_system()
    app.run(host='0.0.0.0', port=5002, debug=True)
