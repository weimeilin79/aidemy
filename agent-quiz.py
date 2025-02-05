import os
from langchain.vectorstores import FAISS
from langchain.embeddings import VertexAIEmbeddings
from vertexai.language_models import TextEmbeddingModel
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.memory import MemoryVectorStore

# Load PDF
loader = PyPDFLoader("your_pdf_file.pdf") #replace with your pdf file
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Generate embeddings
embeddings = VertexAIEmbeddings()

#Store in memory
vectorstore = MemoryVectorStore.from_documents(docs, embeddings)

def find_similar_curriculum():
    return aaa