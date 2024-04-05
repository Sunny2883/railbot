"""get all the llm models and embedding models here"""

import os
import dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings

# load all the secrets, api keys
dotenv.load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")


# load openai llm model
chat_llm_model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2, api_key=openai_api_key)

# load openai embedding model
embedding_model_o = OpenAIEmbeddings()

# load google generative ai model
google_llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=google_api_key,
    convert_system_message_to_human=True,
)

# load huggingface embedding model
embedding_model_hf = HuggingFaceEmbeddings()
