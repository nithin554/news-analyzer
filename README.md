# News Analyzer Agent

[![Pull Request](https://github.com/nithin554/news-analyzer/actions/workflows/pull-request.yml/badge.svg)](https://github.com/nithin554/news-analyzer/actions/workflows/pull-request.yml)
[![Merge](https://github.com/nithin554/news-analyzer/actions/workflows/push.yml/badge.svg)](https://github.com/nithin554/news-analyzer/actions/workflows/push.yml)
[![Generate Report](https://github.com/nithin554/news-analyzer/actions/workflows/generate-report.yml/badge.svg)](https://github.com/nithin554/news-analyzer/actions/workflows/generate-report.yml)   

This project is a Generative AI News Analyzer Agent that automatically gathers, processes, and summarizes recent information from bbc.co.uk, and then provides a simple way for users to chat with the system about the data collected.

It uses Newspaper3k, BeautifulSoup, Gemini, LangChain (LLM Orchestration), LangSmith (Tracing), MongoDB (Vector Database) and Streamlit. 

## Instructions to Run

### Docker
   ```bash
   docker pull ghcr.io/nithin554/news-analyzer:latest
   docker run -d --name news-analyzer -p 8501:8501 ghcr.io/nithin554/news-analyzer:latest
   ```
   This runs streamlit on port 8501 and can be accessed via `http://localhost:8501/`
### Python

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the chatbot application:
   ```bash
   python main.py chatbot
   ```
   This runs streamlit on port 8501 and can be accessed via `http://localhost:8501/`
3. Run the reporting application (Run this for the first time to prepare the data):
   ```bash
   python main.py report
   ```
   This scrapes news articles and prepares vector embeddings which are them uploaded to MongoDB. Also creates a summary of all the news articles scraped.
4. Run reporting and chatbot
   ```bash
   python main.py
   ```
   This creates a scheduler that runs every hour updating the articles in the database meanwhile runs a chatbot using streamlit parallely.
