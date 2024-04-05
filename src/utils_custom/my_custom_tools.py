"""All the main tools used by langchain agent is here"""

from langchain.tools import StructuredTool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import Chroma

from .models import embedding_model_hf
from .constants import CHROMA_COLLECTION_NAME, CHROMA_STORAGE_PATH

# duck duck go search
search = DuckDuckGoSearchRun()


# retriever tool
db = Chroma(
    persist_directory=CHROMA_STORAGE_PATH,
    embedding_function=embedding_model_hf,
    collection_name=CHROMA_COLLECTION_NAME,
)
retriever = db.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    "knowledge_base_search",
    "Search for information about train from knowledgebase using this tool!",
)


# tool for calculating fare
def calculate_fare(dist: float, fare_per_km: float):
    """Calculates fare for a passeger based on distances between stations and booked seat type"""
    fare = dist * fare_per_km
    return fare

calculate_fare = StructuredTool.from_function(
    func=calculate_fare,
    name="calculate_fare",
    description="Calculates fare for a passeger based on distances between stations and booked seat type. It takes two arguments distance between the stations and fare per km for particular seat type. It returns the total fare. use calculate distance tool to get distance and retriever tool to get fare per km for particular seat type before using this tool.",
)


# tool for calculating distance
def calculate_distance(dist_station1: float, dist_station2: float):
    """Calculates distance between two stations based on their distance from a particular place. at first gather the distances of each station from a particular place from knowledgebase or web search if not available in knowledgebase, then use this tool to calculate the distance between them"""
    dist = abs(dist_station1 - dist_station2)
    return dist

calculate_distance = StructuredTool.from_function(
    func=calculate_distance,
    name="calculate_distance",
    description="Calculates distance between two stations based on their distance from a particular place. at first gather the distances of each station from a particular place from knowledgebase or web search if not available in knowledgebase, then use this tool to calculate the distance between them",
)


# list of all tools
tools = [search, retriever_tool, calculate_fare, calculate_distance]
