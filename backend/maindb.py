from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
import mongodData
import pandas as pd

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# Iterate through PDFs and collect text chunks
def get_text_chunks_from_folder(folder_path):
    text_chunks = []
    # Iterate through each PDF and extract text
    for pdf_file in os.listdir(folder_path):
        if pdf_file.endswith('.pdf'):
            full_path = os.path.join(folder_path, pdf_file)
            text = extract_text_from_pdf(full_path)
            chunks = text.split('\n\n')
            text_chunks.extend(chunks)
    return text_chunks

# Extract chunks from both folders (good and bad PDFs)
good_chunks = get_text_chunks_from_folder('good')
bad_chunks = get_text_chunks_from_folder('bad')

mongo_chunks = mongodData.create_mongo_vectordb()

good_chunks.append(str(mongo_chunks))

# Combine and embed all chunks
all_chunks = good_chunks + bad_chunks
embeddings = model.encode(all_chunks)

# Use FAISS to create a vector index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save metadata (for traceability)
metadata = [{'text': chunk, 'type': 'good' if i < len(good_chunks) else 'bad'}
            for i, chunk in enumerate(all_chunks)]

# Save the FAISS index and metadata
def save_vector_db():
    index_file='vector_index.faiss'
    metadata_file='metadata.pkl'
    # Save the FAISS index
    faiss.write_index(index, index_file)
    # Save the metadata using pickle
    with open(metadata_file, 'wb') as f:
        pickle.dump(metadata, f)
