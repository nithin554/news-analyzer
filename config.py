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
