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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

os.environ["TOKENIZERS_PARALLELISM"] = "false"

api_key = "YOUR_API_KEY"
gapi_key="YOUR_API_KEY"
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

def extract_relevant_sentences(text, question, top_n=2):
    sentences = text.split(". ")
    vectorizer = TfidfVectorizer().fit_transform([question] + sentences)
    vectors = vectorizer.toarray()
    
    # Calculate cosine similarity between the question and sentences
    cosine_similarities = cosine_similarity([vectors[0]], vectors[1:])[0]
    # Get the indices of the top n most similar sentences
    top_indices = cosine_similarities.argsort()[-top_n:][::-1]
    # Concatenate these sentences as the relevant part
    return ". ".join([sentences[idx] for idx in top_indices])

# Query the vector database
def query_vector_db(index, metadata, question, k=2):
    # Encode the question
    question_embedding = model.encode([question])
    # Search the FAISS index
    _, indices = index.search(np.array(question_embedding), k=k)
    # Retrieve and return the closest text chunks
    # results = [metadata[idx]['text'] for idx in indices[0]]
    results = [extract_relevant_sentences(metadata[idx]['text'], question, 5) for idx in indices[0]]
    print(len(results[0]))
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

# maindb.save_vector_db()
# index, metadata = load_vector_db()

def analyze_question(question):
    maindb.save_vector_db()
    index, metadata = load_vector_db()
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
    maindb.save_vector_db()
    index, metadata = load_vector_db()

    queries=check_type_of_pdf(raw_text)

    if len(queries) > 1:
        contentarr=[]
        for query in queries:
            user_question=query
            retrieved_chunks = query_vector_db(index, metadata, user_question,5)
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
