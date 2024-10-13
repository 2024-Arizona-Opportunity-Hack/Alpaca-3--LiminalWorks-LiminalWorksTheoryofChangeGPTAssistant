import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import openai
import os
from PyPDF2 import PdfReader
from createpdf import create_pdf
from pdfcontentreader import check_type_of_pdf
import maindb
import mongodData

os.environ["TOKENIZERS_PARALLELISM"] = "false"

api_key = "YOUR_KEY"
gapi_key="YOUR_KEY"
openai.api_key=api_key
# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the FAISS index and metadata
def load_vector_db(index_file='vector_index.faiss', metadata_file='metadata.pkl'):
    # Load the FAISS index
    index = faiss.read_index(index_file)
    # Load the metadata
    with open(metadata_file, 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata

# Query the vector database
def query_vector_db(index, metadata, question, k=2):
    # Encode the question
    question_embedding = model.encode([question])
    # Search the FAISS index
    _, indices = index.search(np.array(question_embedding), k=k)
    # Retrieve and return the closest text chunks
    results = [metadata[idx]['text'] for idx in indices[0]]
    return results

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def get_text_chunks_from_folder(pdf_file):
    text_chunks = []
    text = extract_text_from_pdf(pdf_file)
    chunks = text.split('\n\n')
    text_chunks.extend(chunks)
    return text_chunks

def content_gen(contentarr):
    create_pdf(contentarr)

def summarize_chunks(retrieved_chunks):
    genai.configure(api_key=gapi_key)
    pt=f"summarize about {retrieved_chunks} in 50 words."
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-exp-0827")
    response = model.generate_content(pt)
    return response.text


def get_gpt_ans(retrieved_chunks, user_question):
    response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"based on Context\n{retrieved_chunks}\nanswer it: {user_question}",
                }
            ],
            max_tokens=100
        )
    response = response.choices[0].message.content
    return response

maindb.save_vector_db()

index, metadata = load_vector_db()

def analyze_question(question):
    if question:
        user_question="check if the given "+question+" is related to Theory of Change. If not deny politely."
        retrieved_chunks = query_vector_db(index, metadata, user_question,5)
        summarized_chunks = summarize_chunks(retrieved_chunks)
        res=get_gpt_ans(summarized_chunks, user_question)
        data = {
                "query": user_question,
                "response": res
        }
        mongodData.insert_data_to_database(data)
        return res

# Main function to demonstrate querying
def analyze_pdf(raw_text):
   
    queries=check_type_of_pdf(raw_text)

    if len(queries) > 1:
        contentarr=[]
        for query in queries:
            user_question=query
            retrieved_chunks = query_vector_db(index, metadata, user_question,2)
            res=get_gpt_ans(retrieved_chunks, user_question)
            data = {
                "query": user_question,
                "response": res
            }
            mongodData.insert_data_to_database(data)
            qr=[user_question, res]
            contentarr.append(qr)
        content_gen(contentarr)
        return "File ready"
        
    else:
        user_question=queries[0]
        retrieved_chunks = query_vector_db(index, metadata, user_question,3)
        summarized_chunks = summarize_chunks(retrieved_chunks)
        res=get_gpt_ans(summarized_chunks, user_question)
        return res
