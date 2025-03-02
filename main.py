import streamlit as st
import os
import base64
from io import BytesIO
from pdfminer.high_level import extract_text
import openai
openai.api_key = "your_token"


models = openai.Model.list()

def pdf_to_text(pdf_file):
    text = extract_text(pdf_file)
    return text

def save_text_to_file(text, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text)

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text_content = file.read()
    return text_content        

st.markdown("""
    <style>
    .title {
        text-align: center;                 
    }
    </style>
""", unsafe_allow_html=True)

text_content = """this is a condidates CV:
    
    """ 

with st.sidebar:
    st.image("https://static.tildacdn.com/tild3263-6531-4764-b532-343666323531/brain1.png")
    st.markdown("<h1 class='title'>RESUME PARSING & JOBS MATCHING</h1>", unsafe_allow_html=True)
    st.sidebar.header("Navigation : ")
    choice = st.sidebar.radio("", ["Upload CV", "CHATBOT", "Jobs Matching"])
    st.sidebar.info("Develop a simple yet accurate CV parsing model and web-app to match candidate profiles with suitable job offers, providing cost-effective and efficient hiring solutions for Moroccan startups and companies. Ensure data privacy by enabling internal usage without sharing sensitive information.")

if choice == "Upload CV":
    st.markdown("<h1 class='title'> Upload PDF File of The Candidate </h1>", unsafe_allow_html=True)
    st.write("Select a PDF file to download:")
    file = st.file_uploader("Download the PDF file", type=["pdf"])
    
    if file is not None:
        pdf_contents = file.read()
        st.success("Successfully downloaded file!")
        # Convert the binary data to a base64 string
        base64_pdf = base64.b64encode(pdf_contents).decode('utf-8')
        # Display the PDF using an HTML <embed> tag with base64 encoded data
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="600" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)
        text_content += pdf_to_text(BytesIO(pdf_contents))
        save_text_to_file(text_content, "text_chatbot.txt")

if choice == "CHATBOT":

    st.markdown("<h1 class='title'>CHATBOT FOR HR </h1>", unsafe_allow_html=True)
    user_input = st.text_area("Enter Your Question Here:", value="", height=100)

    with open("text_chatbot.txt", "r",encoding='utf-8') as f:
        text_content += f.read()
    if st.button('send'):
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user","content":text_content + user_input}])
        
        st.write(f"Chatbot: {chat_completion.choices[0].message.content}")
    
    
if choice == "Jobs Matching":
        st.markdown("<h1 class='title'> Upload PDF File of The Candidates </h1>", unsafe_allow_html=True)
        st.write("Select PDF files to download:")
        files = st.file_uploader("Download the PDF files", type=["pdf"], accept_multiple_files=True)

        if files is not None:
            for file in files:
                pdf_contents = file.read()
                st.success(f"Successfully downloaded file: {file.name}")
                # Convert the binary data to a base64 string
                base64_pdf = base64.b64encode(pdf_contents).decode('utf-8')
                # Display the PDF using an HTML <embed> tag with base64 encoded data
                pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="600" type="application/pdf">'
                st.markdown(pdf_display, unsafe_allow_html=True)
                text_content = pdf_to_text(BytesIO(pdf_contents))
                save_text_to_file(text_content, f"{os.path.splitext(file.name)[0]}.txt")

        st.subheader("Jobs Description")
        user_input = st.text_area("Enter Your Description Here:", value="", height=100)

        prompt = 'extract only the skills of the condidate, it should be in one sentence seperated by commas, no additional text '
        if st.button('Match'):
            for i in range(1,5):
                cv = ""
                with open(f"cv{i}.txt", "r", encoding='utf-8') as f:
                    cv += f.read()
                fprompt = prompt + cv

                chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user","content":fprompt}])
        
                save_text_to_file(chat_completion.choices[0].message.content, f"skills{i}.txt")

            job_d = ""
            with open(f"job_desc.txt", "r", encoding='utf-8') as f:
                job_d += f.read() 
            fprompt = 'extract only the skills needed from this position, it should be in one sentence seperated by commas, no additional text ' + job_d
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user","content":fprompt}])
        
            save_text_to_file(chat_completion.choices[0].message.content, f"skills_jobd.txt")

            import subprocess

            result = subprocess.run(["python", ".\Classify.py"], capture_output=True, text=True)
            output = result.stdout

            # Print the captured output
            print("Captured Output:")
            print(output)
            st.write(f"{output}")

            '''------------------------------------'''
            gene_prompt = 'extract softskills in one single summarized short paragraph, without names, and the discription should be from 2 sentences '

            for i in range(1,4,2):
                cv = ""
                with open(f"cv{i}.txt", "r", encoding='utf-8') as f:
                    cv += f.read()
                fprompt = gene_prompt + cv

                chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user","content":fprompt}])
        
                save_text_to_file(chat_completion.choices[0].message.content, f"softskills{i}.txt")

            job_d = ""
            with open(f"job_desc.txt", "r", encoding='utf-8') as f:
                job_d += f.read() 
            fprompt = 'extract only the soft skills skills needed from this position, it should be in one sentence seperated by commas, no additional text ' + job_d
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user","content":fprompt}])
        
            save_text_to_file(chat_completion.choices[0].message.content, f"soft_skills_jobd.txt")


            result = subprocess.run(["python", ".\Match.py"], capture_output=True, text=True)
            output = result.stdout

            # Print the captured output
            print(output)
            st.write(f"{output}")
