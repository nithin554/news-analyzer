import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.5-flash-lite"

TARGET_URLS = [
    "https://www.bbc.co.uk/news/technology"
]

TOPICS = ["AI", "Artificial Intelligence", "Machine Learning", "Technology", "Economy", "Business"]

DATA_DIR = "data"
REPORT_FILE = os.path.join(DATA_DIR, "latest_report.txt")

VECTOR_DB_NAME = "News_Data"
VECTOR_COLLECTION_NAME = "News_Scrapping_Data"

"""
# LangSmith Tracing Configuration
# Support both LANGCHAIN_TRACING_V2 (standard for LangChain) and LANGSMITH_TRACING
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://eu.api.smith.langchain.com")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "News Analyzer")

if LANGSMITH_TRACING:
    os.environ["LANGSMITH_TRACING"] = "true"
    if LANGSMITH_API_KEY:
        os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_ENDPOINT"] = LANGSMITH_ENDPOINT
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
"""
