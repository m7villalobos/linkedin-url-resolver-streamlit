import streamlit as st
import re
import requests
from bs4 import BeautifulSoup
import json  # For safely serializing the text

# Function to resolve LinkedIn URLs
def extract_final_url(linkedin_url):
    try:
        response = requests.get(linkedin_url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        external_link = soup.find('a', href=True)
        if external_link and external_link['href'].startswith('http'):
            return external_link['href']
        return linkedin_url
    except requests.exceptions.RequestException as e:
        print(f"Error obtaining the URL {linkedin_url}: {e}")
        return linkedin_url

def replace_urls_in_text(text):
    linkedin_urls = re.findall(r"https://lnkd\.in/\S+", text)
    for url in linkedin_urls:
        resolved_url = extract_final_url(url)
        text = text.replace(url, resolved_url)
    return text

# Streamlit interface
st.title("LinkedIn URL Resolver")
# Creator information
st.write("Created by [Miguel Ángel Villalobos García](https://www.linkedin.com/in/m7villalobos/)")
st.write("Paste your LinkedIn post below and this app will replace shortened URLs with their original links.")

# Input text area with more lines visible
input_text = st.text_area("Paste your LinkedIn post here:", height=150)

if st.button("Resolve URLs"):
    if input_text.strip():  # Check if the text is not empty
        resolved_text = replace_urls_in_text(input_text)

        # Display the processed text with more lines
        st.subheader("Processed Text:")
        st.text_area("Updated Post:", resolved_text, height=250, key="output")

        # Escape the processed text for HTML/JavaScript
        escaped_text = json.dumps(resolved_text)

        # Uniform button style
        button_style = """
            display: inline-block;
            width: 100%;
            margin-top: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 10px 12px 10px;
            font-size: 14px;
            cursor: pointer;
        """

        # HTML/JS for copying text to clipboard
        st.components.v1.html(
            f"""
            <script>
            function copyToClipboard() {{
                const text = {escaped_text};
                navigator.clipboard.writeText(text).then(() => {{
                    alert('Text copied to clipboard!');
                }}).catch(err => {{
                    console.error('Error copying to clipboard:', err);
                    alert('Error copying to clipboard. Please try again.');
                }});
            }}
            </script>
            <button onclick="copyToClipboard()" style="{button_style}">
                Copy to Clipboard
            </button>
            """,
            height=100,  # Increased height to avoid cutoff
        )
    else:
        st.error("Please enter text to process.")
