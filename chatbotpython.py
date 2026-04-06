import streamlit as st
import google.generativeai as genai
import os
import random

# ── CONFIG ─────────────────────────────────────────────

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"]))
MODEL = "gemini-2.5-flash"
TXT_FILE = "chatbot.txt"
# ──────────────────────────────────────────────────────

st.set_page_config(page_title="PT LEE CNCET Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0a0d1a; color: #e8eaf6; }
.stApp { background: linear-gradient(135deg, #0a0d1a, #0f1628); }

.user-msg {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    color: white; padding: 12px 16px;
    border-radius: 16px 16px 4px 16px;
    margin: 6px 0; max-width: 78%; margin-left: auto;
    font-size: 14px; line-height: 1.6;
}
.bot-msg {
    background: #1a2444; border: 1px solid #1e2d5a;
    color: #e8eaf6; padding: 12px 16px;
    border-radius: 16px 16px 16px 4px;
    margin: 6px 0; max-width: 78%;
    font-size: 14px; line-height: 1.6;
}
.msg-label { font-size: 11px; color: #7a8ab0; margin-bottom: 3px; }

.stTextInput > div > div > input {
    background: #0f1628 !important;
    border: 1px solid #1e2d5a !important;
    border-radius: 12px !important;
    color: #e8eaf6 !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4f8ef7 !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
}
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #4f8ef7, #a259ff) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-size: 14px !important; font-weight: 600 !important;
    width: 100% !important;
}
.stButton > button {
    background: #1a2444 !important; color: #e8eaf6 !important;
    border: 1px solid #1e2d5a !important; border-radius: 10px !important;
    width: 100% !important;
}
[data-testid="stSidebar"] { background: #0f1628 !important; border-right: 1px solid #1e2d5a !important; }
hr { border-color: #1e2d5a !important; }
</style>
""", unsafe_allow_html=True)

# ── Auto-load chatbot.txt ──────────────────────────────
@st.cache_data
def load_college_data():
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return None

college_data = load_college_data()

# ── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 PT LEE CNCET")
    if college_data:
        st.success("✅ chatbot.txt loaded!")
        st.info(f"📊 {len(college_data)} characters")
    else:
        st.error(f"❌ '{TXT_FILE}' not found!\nPlace chatbot.txt in the same folder as chatbot.py")
    st.divider()
    st.markdown("**Model:** `gemini-2.5-flash`")
    st.markdown("**College:** PT LEE CNCET")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = None
        st.rerun()

# ── Header ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:20px 0 10px;">
  <p style="font-family:'Orbitron',sans-serif; font-size:22px; font-weight:700;
     background:linear-gradient(90deg,#4f8ef7,#a259ff);
     -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;">
    🤖 PT LEE CNCET
  </p>
  <p style="color:#7a8ab0; font-size:13px; margin-top:4px;">Customer Care Assistant</p>
</div>
""", unsafe_allow_html=True)
st.divider()

# ── Session state ──────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = None

# ── Init Gemini chat session ───────────────────────────
if college_data and st.session_state.chat is None:
    system_prompt = f"""
You are PTLEE CNCET Customer care executive. Your job is to provide answers to the questions asked by the customers.
Answer politely. If a question is outside the provided info, say you do not have that information.
Only refer to the provided college information below.

{college_data}
""".strip()
    model_obj = genai.GenerativeModel(model_name=MODEL, system_instruction=system_prompt)
    st.session_state.chat = model_obj.start_chat(history=[])

# ── Display messages ───────────────────────────────────
if not st.session_state.messages:
    if college_data:
        st.markdown("<div class='bot-msg'>👋 Hi! I'm the PT LEE CNCET assistant. Ask me anything about the college!</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>⚠️ Place <b>chatbot.txt</b> in the same folder as chatbot.py and restart.</div>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='msg-label'>You</div><div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='msg-label'>🤖 PT LEE Assistant</div><div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

st.divider()

# ── Input form — Enter key + Send button both work ─────
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            label="message",
            placeholder="Type your question and press Enter ↵ or click Send...",
            label_visibility="collapsed"
        )
    with col2:
        submitted = st.form_submit_button("Send ➤")

# ── Handle submission ──────────────────────────────────
if submitted and user_input.strip():
    if not college_data:
        st.warning("⚠️ chatbot.txt not found. Place it in the same folder as chatbot.py!")
    elif st.session_state.chat is None:
        st.error("Chat not initialized. Please restart.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(user_input.strip())
                reply = response.text
            except Exception as e:
                reply = f"❌ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
