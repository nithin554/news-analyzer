import os

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from config import TOPICS
from mongo_db import MongoDBConnector

# Import from local modules
# Note: When running with streamlit, the working directory might be different,
# so we might need to adjust imports or path.
# For simplicity, we'll assume the script is run from the project root.
try:
    from reporter import load_latest_report
    from config import GOOGLE_API_KEY, MODEL_NAME
except ImportError:
    # Fallback for when running directly if paths are an issue, 
    # but usually running `streamlit run chatbot.py` from root works.
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from reporter import load_latest_report
    from config import GOOGLE_API_KEY, MODEL_NAME

def get_chatbot_response(user_question):
    """
    Generates a response to a user's question based on the latest report.
    """

    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GOOGLE_API_KEY)

    template = """
    Classify the user question into one of the following topics:
    {topics}, greetings, other
    
    Question: {question}
    
    Respond with ONLY the topic name.
    """
    prompt = PromptTemplate(template=template, input_variables=["topics", "question"])
    chain = prompt | llm

    try:
        response = chain.invoke({"topics": ", ".join(TOPICS), "question": user_question})
        topic = response.content
        print(topic)
        if (topic not in TOPICS) and (topic != "greetings"):
            return "Sorry, I only analyze news related to " + ", ".join(TOPICS) + "."
    except Exception as e:
        return f"Error getting response: {e}"

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    connector = MongoDBConnector()
    connector.ping()

    docs = []
    vector_chunks = connector.get_vector_chunks(user_question, embedding_model)
    while vector_chunks.alive:
        chunk = vector_chunks.try_next()
        docs.append(str(chunk.get("text")))

    template = """
    You are a helpful AI assistant which answers questions only about news summaries scraped from bbc.co.uk related to {topics} topics, 
    and refrain from answering other questions unrelated to {topics} topics by politely rejecting the request. 
    If the question is related to {topics} topics, then answer the user's question based on the vector embedding chunks retrieved from the user's query.
    Even if you know the answer to the question, but the question is not related to {topics} topics, politely reject the request.
    If the user asks general greeting question, greet them back politely as a helpful news summarizer AI assistant.
    
    Docs:
    {docs}

    Question:
    {question}
    """
    prompt = PromptTemplate(template=template, input_variables=["topics", "docs", "question"])
    chain = prompt | llm

    try:
        response = chain.invoke({"topics": TOPICS, "docs": docs, "question": user_question})
        return response.content
    except Exception as e:
        return f"Error getting response: {e}"

def run_chatbot():
    st.title("News Analyzer Chatbot")

    # Load the report
    try:
        load_latest_report()
    except Exception as e:
        st.error(f"Error loading report: {e}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question about the latest news..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = get_chatbot_response(prompt)
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    run_chatbot()
