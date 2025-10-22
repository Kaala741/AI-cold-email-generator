import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from streamlit_lottie import st_lottie
import json
import requests

def load_lottiefile(filepath:str):
    with open(filepath,encoding="utf8") as f:
        data =json.load(f)
    return data

lottie_coding = load_lottiefile("app/anime.json")





def create_streamlit_app(llm, portfolio, clean_text):
    st.title("💌 AI-Powered Cold Email Generator")
    st.write("\n\n")
    st.write("---")
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.header(":blue[ABOUT THIS PAGE]")
            st.write(
                """
                This Streamlit app demonstrates an AI-driven Cold Email Generator powered by LLaMA, designed to craft personalized and high-conversion outreach messages instantly. 
                By leveraging advanced natural language processing and contextual understanding, it tailors tone, content, and structure based on your input — whether you’re reaching out for sales, networking, recruitment, or collaborations. 
                The app highlights how large language models can streamline communication workflows, reduce manual effort, and enhance productivity across marketing and business development pipelines.
                 It’s a practical example of how generative AI can transform traditional outreach into a data-driven, scalable, and smarter process.
                """
            )
        with right_column:
            st_lottie(lottie_coding, height=400, key="coding")
    st.write("---")
    st.header("Generate Your Personalized Email")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)