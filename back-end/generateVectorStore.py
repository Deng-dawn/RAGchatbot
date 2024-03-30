import exts
import os
import shutil
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate


# ========== create the database ==========
def generate_data_store_from_website(url=exts.WEBSITE_URL):
    documents = load_documents(url)
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents(url):
    loader = WebBaseLoader(url)
    document = loader.load()
    return document


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=20,
                                                   length_function=len, )
    chunks = text_splitter.split_documents(documents)
    return chunks


def save_to_chroma(chunks):
    # clear existing database
    if os.path.exists(exts.CHROMA_PATH):
        shutil.rmtree(exts.CHROMA_PATH)
    # load chunks into chroma
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=exts.CHROMA_PATH
    )
    db.persist()
    print(f"saved {len(chunks)} to {exts.CHROMA_PATH}")


if __name__ == "__main__":
    generate_data_store_from_website()

