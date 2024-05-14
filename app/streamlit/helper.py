from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
import pandas as pd
import constants as CONSTANTS
import re
from io import BytesIO
import PyPDF2

# Initialize the sentence embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_file(file_stream):
    """
    Extract text from the provided file stream.
    Supports 'text/plain' and 'pdf' file types.
    """
    file_type = file_stream.type
    if 'text/plain' in file_type:
        file_stream.seek(0)
        content = file_stream.read().decode('utf-8')
        return content

    elif 'pdf' in file_type:
        file_stream.seek(0)
        pdf_reader = PyPDF2.PdfReader(file_stream)
        accumulated_text = ''
        for page in pdf_reader.pages:
            accumulated_text += page.extract_text() + '\n'
        return accumulated_text

    else:
        print("Unsupported file format. Acceptable formats include .txt and .pdf.")
        return None

def segment_text(file_path):
    """
    Segments text into chunks from the specified file path, based on its extension.
    """
    if file_path.lower().endswith('.txt'):
        with open(file_path, 'r') as file:
            full_text = file.read()

        text_segmenter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ' ', ''],
            chunk_size=800,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False
        )
        return text_segmenter.create_documents([full_text])

    elif file_path.lower().endswith('.pdf'):
        pdf_loader = PyPDFLoader(file_path)
        documents = pdf_loader.load()
        text_segmenter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = []
        for document in documents:
            chunks.extend(text_segmenter.create_documents([document]))
        return chunks

    else:
        print("Unsupported file format. Acceptable formats include .txt and .pdf.")
        return None

def sanitize_text(raw_text):
    """
    Cleans and standardizes the provided text string by removing unwanted characters
    and fixing common formatting issues.
    """
    try:
        cleaned_text = re.sub(r'[^a-zA-Z0-9 .,;:\'"\(\)\[\]\-]', '', raw_text)
        cleaned_text = re.sub(r'(?<=[.,;:\'"])(?=[^\s])', ' ', cleaned_text)
        cleaned_text = re.sub(r'(?<=[^\s])(?=[.,;:\'"])', ' ', cleaned_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text = re.sub(r'(\d+)([A-Za-z])', r'\1 \2', cleaned_text)
        cleaned_text = re.sub(r'([A-Za-z])(\d+)', r'\1 \2', cleaned_text)
        cleaned_text = cleaned_text.strip()
        return cleaned_text
    except Exception as e:
        print(f"Error while processing text: {e}")
        return raw_text

def create_text_chunks(input_text):
    """
    Creates manageable chunks of text from a larger input text string.
    """
    segmenter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ' ', ''],
        chunk_size=800,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False
    )
    return [sanitize_text(chunk.page_content) for chunk in segmenter.create_documents([input_text])]

def construct_dataframe(text):
    """
    Constructs a dataframe from chunks of text, appending sentence embeddings.
    """
    chunks = create_text_chunks(text)
    df = pd.DataFrame(chunks, columns=["text"])
    embeddings = embedding_model.encode(df['text'].tolist(), normalize_embeddings=True)
    df['text_vector'] = embeddings.tolist()
    return df

def generate_text_embedding(input_text):
    """
    Generates a normalized embedding for a given text string.
    """
    return embedding_model.encode(input_text, normalize_embeddings=True).tolist()

def concatenate_vector_results(results):
    """
    Concatenates a list of strings into a single string.
    """
    return ' '.join(results)
