🚀 PDF-Genie: Turn Your PDFs into a Smart Assistant 🤖📄

Ever wished you could ask questions directly from PDFs instead of scrolling endlessly? Meet PDF-Genie, a Streamlit app that lets you do exactly that!

PDF-Genie transforms your documents into a smart assistant, providing instant, context-aware answers from your PDFs.


✨ Features

📁 Multiple PDF Uploads – Upload and process several PDFs at once.

🧩 Context-Aware Chunking – Break PDFs into meaningful chunks for accurate Q&A.

🤖 Google Gemini AI Powered – Get detailed and relevant answers using the latest LLM.

💾 FAISS Vector Storage – Lightning-fast semantic search for large documents.

⚡ Efficient Document Handling – Optimized for handling large PDFs without slowing down.

✅ Interactive & Easy-to-Use – Built entirely with Python & Streamlit.


🛠 Tech Stack & Libraries

Python & Streamlit – Front-end interactive interface.

pypdf – Extract text from PDF files.

LangChain & LangChain Community – Chains, embeddings, and text processing.

HuggingFace Transformers – Generate sentence embeddings for semantic search.

FAISS – Vector database for high-performance semantic search.

Google Gemini AI – Conversational AI for accurate question answering.

python-dotenv – Manage API keys securely.


💡 Why PDF-Genie?

PDF-Genie is perfect for:

Research papers

Manuals & guides

Reports & documents

Turn them into a smart assistant that answers your questions instantly, saving you hours of reading and scrolling.


🎯 How to Use

Clone the repository:

git clone https://github.com/yourusername/pdf-genie.git
cd pdf-genie


Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


Add your API keys in .env (Google Gemini, if required).

Run the Streamlit app:

streamlit run app.py


Upload your PDFs and start asking questions!


📂 Project Structure
PDF-Genie/
├─ app.py                # Main Streamlit app
├─ requirements.txt      # Python dependencies
├─ .env.example          # Template for API keys
├─ utils/                # Helper functions for processing PDFs and embeddings
├─ README.md             # Project documentation


🔖 License

This project is MIT Licensed – see the LICENSE
 file for details.


📣 Try it Now!

Turn your PDFs into an AI-powered assistant with PDF-Genie and experience the future of document interaction!


🏷️ Hashtags

#Python #Streamlit #AI #LangChain #FAISS #GoogleGemini #MachineLearning #DataScience #PDFChatbot #MultiFileUpload #TechInnovation
