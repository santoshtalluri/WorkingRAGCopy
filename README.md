markdown
Copy code
# 📚 RAG Application (Retrieval-Augmented Generation)

This project is a **Retrieval-Augmented Generation (RAG) system** that allows users to query documents (like resumes) stored in the system. It processes multiple PDFs in the `data/` folder and enables conversational Q&A on the contents of the documents. Users can upload new files, retrain the system, and query it using a user-friendly web interface.

---

## 🚀 **Features**
- **Load Multiple PDF Files**: Automatically loads and processes all PDF files in the `data/` folder.
- **Dynamic File Uploads**: Users can upload new PDF files and retrain the model.
- **Interactive Q&A**: Ask questions about the loaded PDF content.
- **Real-Time File Management**: View and access files currently used in the RAG system.
- **User Notifications**: Get success/error messages, progress indicators, and training status.
- **Secure File Handling**: API keys are stored in a `.env` file, which is excluded from GitHub.

---

## 📁 **Project Structure**
RAG-Application/ ├── data/ # PDF files used for RAG system ├── static/ # CSS, JS files, and other static resources ├── templates/ # HTML files for web interface ├── .gitignore # Files and folders to ignore in Git ├── main.py # Main script to run the RAG app ├── rag.py # RAG logic file for processing and training ├── styles.css # Custom styles for the web interface ├── README.md # This file ├── requirements.txt # Python dependencies for the app └── .env # API keys and other secrets (not included in GitHub)

yaml
Copy code

---

## 🛠️ **Installation**
Follow these steps to set up the project locally on your MacBook Pro M1.

### **1️⃣ Prerequisites**
- **Python 3.9+** (for M1 compatibility)
- **pip** (Python package installer)
- **Git** (for version control)
- **Virtual Environment** (`venv`)

---

### **2️⃣ Installation Steps**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/RAG-Application.git
Navigate into the project folder:

bash
Copy code
cd RAG-Application
Create a virtual environment:

bash
Copy code
python3 -m venv SkTalluri
Activate the virtual environment:

bash
Copy code
source SkTalluri/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables: Create a .env file in the project root and add:

makefile
Copy code
API_KEY=your_openai_api_key
▶️ Usage
Follow these steps to run the application.

Activate your virtual environment (if not already activated):

bash
Copy code
source SkTalluri/bin/activate
Run the main application:

bash
Copy code
python main.py
Open your browser and go to:

arduino
Copy code
http://127.0.0.1:5000
Upload Files:

Upload PDF files via the "Upload File" button.
Or, place PDF files directly in the data/ folder.
Ask Questions:

Type your query in the input box.
Click Ask to receive answers from the system.
Retrain the Model (Optional):

If you upload new files, click the Retrain button to update the RAG system.
📸 Screenshots
Here are some screenshots of the RAG application.

Home Page:

Upload new PDF files.
View current files loaded into the system.
Ask questions via the input box.
File Management:

Uploaded files are displayed with links to view the content.
Users can see the names of the files used to train the system.
Q&A Interface:

Users can query the system and get human-like responses from the loaded PDFs.
📦 Dependencies
The following dependencies are required to run the app:

Flask: Web framework to build the interactive UI.
OpenAI API: To use the ChatGPT model.
Python-dotenv: Load the API key from the .env file.
Langchain: For RAG (Retrieval-Augmented Generation) logic.
pypdf: To parse PDF files.
faiss: Vector search for fast document retrieval.
All these dependencies are listed in requirements.txt.

📝 Environment Variables
The system uses a .env file to store environment variables securely. This file is listed in .gitignore, so it won’t be uploaded to GitHub.

Add the following variables in the .env file:

makefile
Copy code
API_KEY=your_openai_api_key
Note: Replace your_openai_api_key with your actual API key.

🤔 How It Works
Load PDFs: On startup, the app loads all PDF files from the data/ folder.
File Upload: Users can upload new files via the UI.
Text Extraction: PDF content is converted to plain text.
Embedding Creation: Embeddings are generated for each document using OpenAI embeddings.
Vector Storage: Vectors are stored for fast document retrieval.
Querying: When a user asks a question, it finds relevant sections from the PDFs to answer.
🚀 Key Features
Multi-PDF Support: Automatically processes all PDFs in the data/ folder.
Dynamic File Uploads: Upload a new PDF and retrain the system.
Q&A Chatbot: Query your documents directly from the web UI.
File Status Indicators: See which files are being used and track their status.
Responsive Web Interface: A clean, user-friendly UI for seamless use.
📚 Example Queries
"Summarize the experience section of this resume."
"List all the technical skills mentioned in the PDF."
"Which positions has the applicant held in the past?"
🔐 Security
API Key Protection: The .env file stores API keys securely.
File Protection: The .gitignore prevents .env, cache, and system files from being uploaded to GitHub.
🛠️ Development
If you want to modify the system, here are some key files to edit:

File	Description
main.py	The main application logic (Flask app)
rag.py	RAG logic for processing PDFs, embeddings, and retrieval
templates/	HTML files for UI (modify the interface)
static/	CSS, images, and other static files
.env	Environment file for storing API keys
🐛 Common Issues
API Key Error: Ensure .env has the correct key: API_KEY=your_openai_api_key.
No PDF Loaded: Add PDF files to the data/ folder or upload them via the UI.
Retraining Issue: If the retrain button doesn’t work, make sure you’ve uploaded new files.
🙌 Contributing
Want to contribute? Here’s how you can help:

Fork the repository.

Create a feature branch:

bash
Copy code
git checkout -b feature/your-feature-name
Submit a pull request with your changes.

📄 License
This project is licensed under the MIT License. See the LICENSE file for more information.

💬 Contact
If you have any questions, reach out to me on GitHub.

🎉 Thank you for using the RAG Application! 🎉

yaml
Copy code

---

You can copy and paste this file directly into `README.md`. Let me know if you’d like a
