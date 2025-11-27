# ---------------------------------------------------
# IMPORT NECESSARY LIBRARIES
# ---------------------------------------------------
import streamlit as st
import requests


# ---------------------------------------------------
# OLLAMA SETTINGS
# ---------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"

# Add your Ollama model EXACTLY as shown in `ollama list`
MODEL_NAME = "llama3.1:8b"   # ← Paste model name here, e.g. "llama3.2:8b"


# ---------------------------------------------------
# FUNCTION TO CALL LOCAL OLLAMA
# ---------------------------------------------------
def ask_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False         # ← FIX #1 ADDED HERE
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=120)
        res.raise_for_status()
        data = res.json()

        return data.get("response") or data.get("text") or "⚠ No output received."

    except Exception as e:
        return f"❌ ERROR communicating with Ollama: {e}"


# ---------------------------------------------------
# STREAMLIT APP (UI)
# ---------------------------------------------------
st.set_page_config(page_title="Local LLM Chat", page_icon="🤖")

st.title("🤖 Local LLM Chat — Streamlit + Ollama")
st.write("This interface connects to a **locally installed LLM** using Ollama.")


# ---------------------------------------------------
# SESSION STATE FOR CONVERSATION HISTORY
# ---------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------------------------------------------
# SIDEBAR (HISTORY + RESET)
# ---------------------------------------------------
st.sidebar.title("📜 Conversation History")

# show chat history in sidebar
for i, (user_msg, model_msg) in enumerate(st.session_state.chat_history):
    st.sidebar.write(f"**You:** {user_msg} ")
    st.sidebar.write(f"**Model:** {model_msg} ")
    st.sidebar.write("---")

# reset button
if st.sidebar.button("🔄 Reset Conversation"):
    st.session_state.chat_history = []
    st.experimental_rerun()


# ---------------------------------------------------
# MAIN INPUT AREA
# ---------------------------------------------------
user_input = st.text_area("💬 Enter your message:", height=120)

if st.button("Generate Response"):
    if MODEL_NAME.strip() == "":
        st.warning("⚠ Please set your MODEL_NAME first!")
    elif user_input.strip() == "":
        st.warning("⚠ Please enter a message!")
    else:
        with st.spinner("Model is thinking..."):
            model_answer = ask_ollama(user_input)

        # Save conversation
        st.session_state.chat_history.append((user_input, model_answer))

        # Display output
        st.write("### 🧠 Model Response:")
        st.write(model_answer)
        

