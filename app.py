import streamlit as st
from config import Config
from intent_filter import IntentFilter
from ai_engine import AIEngine
from response_guard import ResponseGuard
from keep_alive import start_keep_alive

# Start background keep-alive ping for Render
start_keep_alive()

# --------------------------------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------------------------------
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------------------------
# SUBTLE NATIVE STYLING
# --------------------------------------------------------------------------
st.markdown("""
<style>
    /* Gentle shadow and border for chat messages */
    div[data-testid="stChatMessage"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        margin-bottom: 1rem;
        transition: box-shadow 0.2s ease;
    }
    div[data-testid="stChatMessage"]:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    
    /* Differentiate AI vs User slightly */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f8fafc;
        border-color: #e2e8f0;
    }

    /* Subtle shadow for avatars */
    div[data-testid="stChatAvatar"] {
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }

    /* Expander styling */
    div[data-testid="stExpander"] {
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------------------------------
# Initialize chat history for UI display only (AI remains stateless)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_api_key' not in st.session_state:
    st.session_state.user_api_key = None

# --------------------------------------------------------------------------
# HEADER SECTION
# --------------------------------------------------------------------------
st.title("⚖️ Judicial Explainer Bot")
st.markdown("Your AI-powered guide to understanding Indian judicial processes and case flows.")

with st.expander("ℹ️ **About & Limitations**", expanded=True):
    st.info("""
    **Welcome!** This bot is designed to educate and explain procedural aspects of the Indian Judicial System.
    
    **What it CAN do:**
    - Explain how to file a case (e.g., FIR, Civil Suit).
    - Describe the stages of a court trial.
    - Define legal terms and roles (e.g., Summons, Bail, Magistrate).
    
    **What it CANNOT do:**
    - Provide legal advice or opinions on your specific case.
    - Guarantee case outcomes.
    - Replace a qualified legal professional.
    """)

# --------------------------------------------------------------------------
# SIDEBAR CONFIGURATION
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.markdown("### API Key Setup")
    with st.form("api_key_form"):
        key_input = st.text_input("Enter Gemini API Key", type="password", help="Required to generate AI responses.")
        submitted = st.form_submit_button("Save Key")
        if submitted:
            st.session_state.user_api_key = key_input
            st.success("API Key saved successfully!")
            
    st.markdown("---")
    st.markdown("### Quick Questions")
    if st.button("How to file an FIR?"):
        st.session_state.prefill_query = "How to file an FIR?"
    if st.button("What is anticipatory bail?"):
        st.session_state.prefill_query = "What is anticipatory bail?"
    if st.button("Stages of a civil suit"):
        st.session_state.prefill_query = "What are the stages of a civil suit?"

# Handle quick question prefilling
initial_input = ""
if "prefill_query" in st.session_state:
    initial_input = st.session_state.prefill_query
    del st.session_state.prefill_query

st.divider()

# --------------------------------------------------------------------------
# CHAT HISTORY DISPLAY
# --------------------------------------------------------------------------
for msg in st.session_state.chat_history:
    avatar = "👤" if msg['role'] == 'user' else "⚖️"
    with st.chat_message(msg['role'], avatar=avatar):
        if msg.get('type') == 'blocked':
            st.error(f"**Request Blocked:**\n\n{msg['message']}")
        elif msg.get('type') == 'compliance':
            st.warning(f"**Compliance Alert:**\n\n{msg['message']}")
        else:
            st.markdown(msg['message'])

# --------------------------------------------------------------------------
# CHAT INPUT & PROCESSING
# --------------------------------------------------------------------------
prompt = st.chat_input("Ask your question... (e.g., What is a summons?)")

# If the user clicked a sidebar button, we process that. If they typed, process that.
query_to_process = prompt if prompt else initial_input

if query_to_process:
    if not query_to_process.strip():
        st.warning("⚠️ Please enter a question to continue.")
    else:
        # 1. Display user message immediately
        st.session_state.chat_history.append({
            'role': 'user',
            'message': query_to_process,
            'type': 'user'
        })
        with st.chat_message("user", avatar="👤"):
            st.markdown(query_to_process)
            
        # 2. Process Assistant Response
        with st.chat_message("assistant", avatar="⚖️"):
            # Use native st.spinner for loading state
            with st.spinner("Analyzing your question..."):
                
                # LAYER 1: INPUT INTENT FILTER
                if not IntentFilter.is_safe(query_to_process):
                    refusal_msg = IntentFilter.get_refusal_message()
                    st.error(f"**Request Blocked:**\n\n{refusal_msg}")
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'message': refusal_msg,
                        'type': 'blocked'
                    })
                else:
                    # LAYER 2: AI ENGINE
                    api_key_to_use = st.session_state.user_api_key
                    raw_response = AIEngine.get_explanation(query_to_process, api_key=api_key_to_use)
                    
                    # LAYER 3: RESPONSE GUARD
                    final_response = ResponseGuard.validate_output(raw_response)
                    
                    if final_response == ResponseGuard.BLOCK_MESSAGE:
                        st.warning(f"**Compliance Alert:**\n\n{final_response}")
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'message': final_response,
                            'type': 'compliance'
                        })
                    else:
                        st.markdown(final_response)
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'message': final_response,
                            'type': 'success'
                        })

# --------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------
st.markdown("---")
st.caption("Built for public legal awareness using responsible AI principles. This application provides procedural education only and does not offer legal advice.")
