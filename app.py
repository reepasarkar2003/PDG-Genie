import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from pathlib import Path

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    st.success("✅ Google Gemini API Connected!")
else:
    st.error("⚠️ GOOGLE_API_KEY not found in .env file")

# ---------------------- PDF Processing ----------------------
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

# ---------------------- Conversational Chain ----------------------
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context.
    If the answer is not in provided context, say "answer is not available in the context".
    
    Context:\n {context}\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# ---------------------- User Input ----------------------
def user_input(user_question):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # ⚠️ Allow pickle deserialization for local vector store
    new_db = FAISS.load_local(
        "faiss_index", 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("**🤖 Reply:**", response["output_text"])

# ---------------------- Main App ----------------------
def main():
    st.set_page_config("Chat PDF", layout="wide")
    st.header("📚 Chat with PDF using PDF-Genie 🤖")

    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

    faiss_exists = os.path.exists("faiss_index")
    
    if faiss_exists:
        user_question = st.text_input("Ask a Question from the PDF Files")
        if user_question:
            with st.spinner("Thinking..."):
                user_input(user_question)
    else:
        st.info("📁 Please upload and process PDFs first to start chatting!")

    with st.sidebar:
        st.title("⚙️ Menu")
        if os.getenv("GOOGLE_API_KEY"):
            st.success("✅ API Key Loaded")
        else:
            st.warning("⚠️ Add GOOGLE_API_KEY to .env file")
        
        st.markdown("---")
        
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True, type="pdf")
        
        if st.session_state.processing_complete:
            button_label = "✅ Processing Complete!"
            button_type = "secondary"
        else:
            button_label = "🚀 Submit & Process"
            button_type = "primary"
        
        if st.button(button_label, type=button_type, use_container_width=True):
            if pdf_docs:
                with st.spinner("Processing PDFs..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.session_state.processing_complete = True
                    st.success(f"✅ Processed {len(pdf_docs)} PDF(s)!")
                    st.balloons()
                    st.rerun()
            else:
                st.warning("Please upload PDF files first")
                st.session_state.processing_complete = False

if __name__ == "__main__":
    main()
