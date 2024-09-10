import streamlit as st
import subprocess

def main():
    st.title("LinkedIn Job Scraper")
    st.write("This application scrapes job postings from LinkedIn based on user-defined criteria.")

    clients = st.text_area("Enter client names (one per line)")

    start_scraping = st.button("Start Scraping")

    if start_scraping:
        subprocess.run(['jupyter', 'nbconvert', '--to', 'script', 'web.ipynb'])  # Convert the notebook to a script
        subprocess.run(['python', 'web.py'])  # Execute the Python script generated from the notebook
        st.write("Scraping is in progress. Please wait for it to complete.")

if __name__ == "__main__":
    main()
