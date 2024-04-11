
import requests
import html2text
from googlesearch import search
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.document_transformers import Html2TextTransformer
import streamlit as st
import google.generativeai as genai


links = []

query = ""
companyName = ""
model_response = ""
content = ""


def setup_apikey(key):
    try:
        GOOGLE_API_KEY = key
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception as e:
        st.error(f"Error setting up API key: {e}")



def web_scrape_now():
    global content
    success = False
    try:
        loader = AsyncHtmlLoader([model_response])
        docs = loader.load()
        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(docs)

        if docs_transformed:
            content = docs_transformed[0].page_content[0:]
            success = True
        else:
            content = ""
    except Exception as e:
        st.error(f"Error scraping web content: {e}")

    return success


def findCorrectLink(links):
    global model_response
    try:
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        prompt = f"\n\nAmong all of these links which one seems to be the correct link for the terms and conditions page? Find only one that is most similar. Dont give any explanation - only give correct answer. Here are they: {', '.join(links)}"
        response = model.generate_content(prompt)  
        model_response = response.text
        web_scrape_now()
    except Exception as e:
        st.error(f"Error finding correct link: {e}")
        return False

def got_query_nowSearch(compName):
    global links
    global companyName
    try:
        links = []
        query =compName+ " terms and conditions"
        companyName = compName

        for results in search(query, 4):
            links.append(results)

        success = findCorrectLink(links)
        if success:
            start_model_response()
            pass


    except Exception as e:
        st.error(f"Error searching query: {e}")
        


def start_model_response():
   try:
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        prompt = f"\nHeres the document taken from the terms and conditions page of a website, you need to answer the questions of the user based on this. provide short and concise answers. dont reply anything now. heres the document content: " + content
        response = model.generate_content(prompt)

   except Exception as e:
       st.error("Something went wrong with Gemini Setup")
           

def get_model_response_with_context_for_question(user_asked):
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    
    user_question = user_asked
    prompt = f"\n user had given the following question, use the document that i provided you earlier to answer it, provide answer in 2 to 3 sentence not more- cover only main points. speak as if youre reprsenting the company named ",companyName,", heres the document:  ",content, "\n\nheres the question: ",user_question

    response = model.generate_content(prompt)
    return response.text
   