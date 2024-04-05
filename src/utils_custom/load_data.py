"""this module has been used to load data using langchain
 document loaders and process them properly
 """

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
    UnstructuredFileLoader,
    UnstructuredPowerPointLoader,
    UnstructuredMarkdownLoader,
)
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from .models import embedding_model_hf
from .constants import CHROMA_COLLECTION_NAME, CHROMA_STORAGE_PATH

def load_file(file):
    """loads file using document loaders like textloader and pypdfloader,
    then splits documents
    and stores them in a chroma database
    arguments:
    file: file path of the file to be loaded
    """
    if ".txt" in file:
        print("loading text file")
        loader = TextLoader(file)
    elif ".pdf" in file:
        print("loading pdf file")
        loader = PyPDFLoader(file)
    elif ".csv" in file:
        print("loading csv file")
        loader = CSVLoader(file)
    elif ".xlsx" in file:
        print("loading xlsx file")
        loader = UnstructuredExcelLoader(file)
    elif ".pptx" in file:
        print("loading pptx file")
        loader = UnstructuredPowerPointLoader(file)
    elif ".docx" in file:
        try:
            print("loading docx file from docx2txt")
            loader = Docx2txtLoader(file)
        except:
            print("loading docx file from unstructured")
            loader = UnstructuredWordDocumentLoader(file)
    elif ".md" in file:
        print("loading markdown file")
        loader = UnstructuredMarkdownLoader(file)
    else:
        print("loading files plus ..")
        loader = UnstructuredFileLoader(file)

    doc = None
    try:
        doc = loader.load()
        print("loading successful...")
    except Exception as e:
        print("loading failed...")
        print(e)

    if doc is None:
        return False

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(doc)

    db = Chroma.from_documents(
        texts,
        embedding=embedding_model_hf,
        persist_directory=CHROMA_STORAGE_PATH,
        collection_name=CHROMA_COLLECTION_NAME,
    )

    print(db)
    return True
