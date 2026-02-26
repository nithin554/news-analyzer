import os

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GOOGLE_API_KEY, MODEL_NAME, REPORT_FILE


def generate_report(articles):
    """
    Generates a report from a list of article texts using Gemini.
    """
    if not articles:
        return "No articles found to generate a report."

    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GOOGLE_API_KEY)

    # Combine article texts (limit to a reasonable length to avoid token limits if necessary, though Gemini has a large context window)
    combined_text = "\n\n".join(articles[:5]) # Limit to first 5 articles for now to be safe and fast

    template = """
    You are a helpful AI assistant that summarizes news articles.
    Please read the following text and generate a report with the following sections:
    1. A 100–150 word summary paragraph.
    2. 3–5 key takeaways.
    3. Mentioned organizations, terms, or key topics.

    Text:
    {text}
    """
    prompt = PromptTemplate(template=template, input_variables=["text"])
    chain = prompt | llm

    try:
        response = chain.invoke({"text": combined_text})
        return response.content
    except Exception as e:
        return f"Error generating report: {e}"

def save_report(report_content):
    """
    Saves the generated report to a file.
    """

    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w") as f:
        f.write(report_content)

def load_latest_report():
    """
    Loads the latest report from the file.
    """
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            return f.read()
    return "No report available yet."
