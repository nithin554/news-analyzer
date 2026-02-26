import hashlib
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from apscheduler.schedulers.blocking import BlockingScheduler
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo.errors import DuplicateKeyError

from config import TARGET_URLS, DATA_DIR
from mongo_db import MongoDBConnector
from reporter import generate_report, save_report
from scraper import scrape_articles


def insert_vector_embeddings(article):
    connector = MongoDBConnector()
    connector.ping()
    collection = connector.get_vector_collection()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = splitter.split_text(article)

    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    futures = []
    for chunk in chunks:
        embedding_vector = embeddings_model.embed_query(chunk)
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures.append(executor.submit(upload_doc, collection, chunk, embedding_vector))

    for future in futures:
        future.result()

def upload_doc(collection, chunk, embedding_vector):
    try:
        collection.update_one(
            {
                "hash": hashlib.md5(chunk.encode("utf-8")).hexdigest()
            },
            {
                "$setOnInsert": {
                    "text": chunk,
                    "embedding": embedding_vector,
                    "source": "news_scraper"
                }
            },
            upsert=True
        )
    except DuplicateKeyError:
        pass

def data_collection_and_reporting_job():
    """
    The job that scrapes articles, generates a report, and saves it.
    """
    print("Starting data collection and reporting job...")
    articles = scrape_articles(TARGET_URLS)
    no_of_articles = str(len(articles))
    print("Collected {no_of_articles} articles.".replace("{no_of_articles}", no_of_articles))
    for article in articles:
        insert_vector_embeddings(article)

    report = generate_report(articles)
    save_report(report)
    print("Data collection and reporting job finished.")

def main():
    """
    Test MongoDB Connector
    """
    MongoDBConnector().ping()

    """
    Main function to run the News Analyzer Agent.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    if len(sys.argv) > 1 and sys.argv[1] == "chatbot":
        # Use subprocess to run the streamlit app
        # This is a common way to launch streamlit from a main script
        try:
            subprocess.run(["streamlit", "run", "chatbot.py"], check=True)
        except FileNotFoundError:
            print("Error: `streamlit` command not found.")
            print("Please make sure Streamlit is installed and in your PATH.")
        except subprocess.CalledProcessError as e:
            print(f"Error running Streamlit app: {e}")

    elif len(sys.argv) > 1 and sys.argv[1] == "report":
        data_collection_and_reporting_job()
    else:
        scheduler = BlockingScheduler()
        # Run the job immediately for the first time
        data_collection_and_reporting_job()
        # Then schedule it to run every hour
        scheduler.add_job(data_collection_and_reporting_job, 'interval', hours=1)
        print("News Analyzer Agent started. Scheduled to run every hour.")
        print("Press Ctrl+C to exit.")
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

if __name__ == "__main__":
    main()
