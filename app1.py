import streamlit as st
from ibm_watsonx_ai.foundation_models import Model
import fitz  # PyMuPDF for PDF reading
import json

# --- IBM Watsonx Credentials ---
api_key = 
project_id = 
base_url = 
model_id =   # ✅ Supported model

# --- Streamlit App Configuration ---
st.set_page_config(page_title="SmartSDLC – AI Assistant", layout="wide")
st.title("🤖 SmartSDLC – AI-Enhanced Software Development Lifecycle")
st.markdown("""
SmartSDLC is a full-stack AI platform that redefines traditional SDLC by automating key stages like requirement classification, code generation, bug fixing, testing, and chatbot support using IBM Watsonx.
""")

# --- Chat history (for chatbot only) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar Menu ---
st.sidebar.title("🧠 SmartSDLC Modules")
module = st.sidebar.radio("Choose a module", [
    "Requirement Upload and Classification",
    "AI Code Generator",
    "Bug Fixer",
    "Test Case Generator",
    "Code Summarizer",
    "Floating AI Chatbot Assistant"
])

# --- Watsonx Query Function ---
def ask_watsonx(prompt):
    try:
        model = Model(
            model_id=model_id,
            credentials={"apikey": api_key, "url": base_url},
            project_id=project_id
        )

        result = model.generate_text(
            prompt=prompt,
            params={
                "max_new_tokens": 500,
                "temperature": 0.7,
                "top_p": 1.0,
                "decoding_method": "sample"
            }
        )

        if isinstance(result, dict):
            return result.get("generated_text", "⚠️ No 'generated_text' in response.")
        elif isinstance(result, str):
            try:
                parsed = json.loads(result)
                return parsed.get("generated_text", result)
            except json.JSONDecodeError:
                return result
        else:
            return "⚠️ Unexpected response type."

    except Exception as e:
        return f"❌ Watsonx Error: {str(e)}"

# --- Module 1: Requirement Classification ---
if module == "Requirement Upload and Classification":
    st.subheader("📄 Upload Requirement PDF")
    file = st.file_uploader("Upload a PDF file", type="pdf")
    if file:
        text = ""
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        st.success("✅ Extracted text from PDF.")
        prompt = f"Classify the following requirements into SDLC phases (Requirement, Design, Development, Testing, Deployment):\n{text}"
        result = ask_watsonx(prompt)
        st.text_area("📋 SDLC Classification", result, height=300)

# --- Module 2: AI Code Generator ---
elif module == "AI Code Generator":
    st.subheader("💡 Generate Production Code")
    user_input = st.text_area("Enter your feature description or user story")
    if st.button("Generate Code") and user_input:
        prompt = f"Generate production-ready Python code for the following description:\n{user_input}"
        result = ask_watsonx(prompt)
        st.code(result, language="python")

# --- Module 3: Bug Fixer ---
elif module == "Bug Fixer":
    st.subheader("🐞 Fix Buggy Code")
    buggy_code = st.text_area("Paste buggy Python or JS code")
    if st.button("Fix Code") and buggy_code:
        prompt = f"Here is some buggy code. Identify and fix the issues:\n{buggy_code}"
        result = ask_watsonx(prompt)
        st.code(result, language="python")

# --- Module 4: Test Case Generator ---
elif module == "Test Case Generator":
    st.subheader("🧪 Generate Unit Tests")
    test_input = st.text_area("Paste code or describe what needs to be tested")
    if st.button("Generate Tests") and test_input:
        prompt = f"Write unit test cases (using unittest or pytest) for the following:\n{test_input}"
        result = ask_watsonx(prompt)
        st.code(result, language="python")

# --- Module 5: Code Summarizer ---
elif module == "Code Summarizer":
    st.subheader("📄 Summarize Code")
    code_to_summarize = st.text_area("Paste code to understand its functionality")
    if st.button("Summarize Code") and code_to_summarize:
        prompt = f"Explain what the following code does:\n{code_to_summarize}"
        result = ask_watsonx(prompt)
        st.text_area("🧠 Code Summary", result, height=200)

# --- Module 6: Floating Chatbot ---
elif module == "Floating AI Chatbot Assistant":
    st.subheader("💬 Ask Anything About SDLC")
    user_query = st.chat_input("Ask about SDLC phases, tools, practices, etc.")
    if user_query:
        st.session_state.chat_history.append(("user", user_query))
        response = ask_watsonx(f"User: {user_query}\nAssistant:")
        st.session_state.chat_history.append(("assistant", response))

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

