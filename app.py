import streamlit as st
from summarizer import extract_keywords, extract_text_from_url, extract_text_with_newspaper, get_sentiment, summarize_with_bart

st.title("Content Summarizer")
input_type = st.radio("Input type:", ("URL", "Text", "PDF"))

if input_type == "PDF":   
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file:
        if st.button("Summarize"):
             with st.spinner("Extracting and summarizing..."):
                import PyPDF2  
                st.subheader("Summary")
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = "".join([page.extract_text() for page in pdf_reader.pages])
                st.write(summarize_with_bart(text))
                st.subheader("Sentiment")
                st.write(get_sentiment(text))
                st.subheader("Keywords")
                st.write(extract_keywords(text))
elif input_type == "URL":
    urls = st.text_area("Enter URLs (one per line):").split("\n")
    if st.button("Summarize"):
        for url in urls:
            if url.strip():
                with st.spinner("Extracting and summarizing..."):
                    text = extract_text_from_url(url)
                    text.join(extract_text_with_newspaper(url))
                    if "Error" not in text:
                        st.subheader("Summary")
                        st.write(summarize_with_bart(text))
                        st.subheader("Sentiment")
                        st.write(get_sentiment(text))
                        st.subheader("Keywords")
                        st.write(extract_keywords(text))
                    else:
                        st.error(text)
        else:
            st.warning("Please enter a valid URL.")
else:
    text = st.text_area("Paste article text:")
    if st.button("Summarize"):
        if text:
            with st.spinner("Summarizing..."):
                st.subheader("Summary")
                st.write(summarize_with_bart(text))
                st.subheader("Sentiment")
                st.write(get_sentiment(text))
                st.subheader("Keywords")
                st.write(extract_keywords(text))
        else:
            st.warning("Please enter some text.")