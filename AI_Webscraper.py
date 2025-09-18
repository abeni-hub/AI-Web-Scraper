import requests
from bs4 import BeautifulSoup
import json
import streamlit as st
from langchain_ollama import OllamaLLM

# Load AI Model

llm = OllamaLLM(model="mistral")

# Function to scrape website 
def scrape_website(url):
    try:
        st.write(f"Scraping Websites: {url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return f"Failed to retrieve the webpage. Status code: {response.status_code}"
        
        # Extract text content
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all("p")
        text = " ".join([para.get_text() for para in paragraphs])

        return text[:2000]
    except Exception as e:
        return f"Error occurred: {str(e)}"
    
# Function to generate summary using AI model
def summarize_content(content):
    st.write("Generating Summary...")
    return llm.invoke(f"Summarize the following content in a concise manner:\n\n{content[:1000]}")

# Streamlit UI
st.title("AI_Powered Web Scraper ")
st.write("Enter a URL to scrape and summarize its content.")


url = st.text_input("Website URL", "https://example.com")
if url:
    content = scrape_website(url)

    if "Failed " in content or "Error " in content:
        st.error(content)
    else:
        summary = summarize_content(content)
        st.subheader("Summary")
        st.write(summary)    