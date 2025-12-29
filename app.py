import streamlit as st
from config import Config
from intent_filter import IntentFilter
from ai_engine import AIEngine
from response_guard import ResponseGuard

# --------------------------------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------------------------------
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------------------------------
# Initialize chat history for UI display only (AI remains stateless)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------------------------------
# CUSTOM CSS STYLING - PREMIUM LIGHT-THEMED PROFESSIONAL DESIGN
# --------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* ============================================
       MAIN APP BACKGROUND - LIGHT THEME
       ============================================ */
    .stApp {
        background: #F8F9FA;
        background-attachment: fixed;
    }
    
    /* Hide Streamlit branding and decorations */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main content container */
    .main .block-container {
        max-width: 850px;
        padding-top: 2rem !important;
        padding-bottom: 3rem;
    }
    
    /* ============================================
       HEADER CARD SECTION
       ============================================ */
    .header-card {
        background: #FFFFFF;
        padding: 30px 40px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #E0E4E8;
        text-align: center;
    }
    
    .header-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 12px;
        line-height: 1.3;
    }
    
    .header-subtitle {
        font-size: 1rem;
        font-weight: 400;
        color: #6B7280;
        line-height: 1.6;
    }
    
    /* ============================================
       LEGAL NOTICE BOX
       ============================================ */
    .legal-notice-box {
        background: #FEF3C7;
        padding: 24px 28px;
        border-radius: 12px;
        margin-bottom: 28px;
        border: 2px solid #F59E0B;
        box-shadow: 0 2px 6px rgba(245, 158, 11, 0.15);
    }
    
    .legal-notice-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #92400E;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .legal-notice-text {
        font-size: 0.95rem;
        font-weight: 500;
        color: #78350F;
        line-height: 1.7;
    }
    
    /* ============================================
       CHAT HISTORY AREA
       ============================================ */
    .chat-history-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 20px;
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E0E4E8;
        margin-bottom: 20px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
    }
    
    .chat-history-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-history-container::-webkit-scrollbar-track {
        background: #F3F4F6;
        border-radius: 4px;
    }
    
    .chat-history-container::-webkit-scrollbar-thumb {
        background: #D1D5DB;
        border-radius: 4px;
    }
    
    .chat-history-container::-webkit-scrollbar-thumb:hover {
        background: #9CA3AF;
    }
    
    /* User Message Bubble - Right Aligned, Light Blue */
    .chat-message-user {
        background: #DBEAFE;
        padding: 16px 18px;
        border-radius: 16px 16px 4px 16px;
        margin: 12px 0 12px 60px;
        text-align: left;
        border: 1px solid #BFDBFE;
        box-shadow: 0 1px 3px rgba(59, 130, 246, 0.1);
    }
    
    .chat-message-user-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #1E40AF;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .chat-message-user-text {
        font-size: 1rem;
        font-weight: 400;
        color: #1F2937;
        line-height: 1.6;
    }
    
    /* Bot Message Bubble - Left Aligned, White with Border */
    .chat-message-bot {
        background: #FFFFFF;
        padding: 16px 18px;
        border-radius: 16px 16px 16px 4px;
        margin: 12px 60px 12px 0;
        text-align: left;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    .chat-message-bot-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #059669;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .chat-message-bot-text {
        font-size: 1rem;
        font-weight: 400;
        color: #1F2937;
        line-height: 1.7;
    }
    
    /* Blocked/Compliance Messages */
    .chat-message-blocked {
        background: #FEE2E2;
        border: 1px solid #FCA5A5;
        padding: 16px 18px;
        border-radius: 12px;
        margin: 12px 60px 12px 0;
    }
    
    .chat-message-compliance {
        background: #FEF3C7;
        border: 1px solid #FDE68A;
        padding: 16px 18px;
        border-radius: 12px;
        margin: 12px 60px 12px 0;
    }
    
    /* ============================================
       INPUT BAR SECTION
       ============================================ */
    .input-container {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E0E4E8;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        margin-bottom: 24px;
    }
    
    .input-label {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 12px;
        display: block;
    }
    
    /* Input field styling - Scoped to Chat Input specifically */
    .input-container .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #E0E4E8;
        padding: 16px 18px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #FFFFFF;
        color: #1F2937 !important;
        caret-color: #3B82F6;
    }
    
    .input-container .stTextInput > div > div > input::placeholder {
        color: #9CA3AF;
        font-weight: 400;
    }
    
    .input-container .stTextInput > div > div > input:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        outline: none;
    }

    /* Standard styling for API Key Input (cleaner, less padding) */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #E0E4E8;
        padding: 8px 12px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 40px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        width: 100%;
        letter-spacing: 0.3px;
        margin-top: 12px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ============================================
       FOOTER SECTION
       ============================================ */
    .footer-box {
        background: #F3F4F6;
        padding: 20px 24px;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        text-align: center;
        margin-top: 32px;
    }
    
    .footer-disclaimer {
        font-size: 0.9rem;
        font-weight: 500;
        color: #4B5563;
        margin-bottom: 8px;
        line-height: 1.6;
    }
    
    .footer-credits {
        font-size: 0.85rem;
        font-weight: 400;
        color: #6B7280;
        line-height: 1.5;
    }
    
    /* ============================================
       EMPTY STATE
       ============================================ */
    .empty-state {
        text-align: center;
        padding: 40px 20px;
        color: #9CA3AF;
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 12px;
    }
    
    .empty-state-text {
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* ============================================
       MOBILE RESPONSIVENESS
       ============================================ */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.5rem;
        }
        
        .header-subtitle {
            font-size: 0.9rem;
        }
        
        .header-card {
            padding: 20px 24px;
        }
        
        .legal-notice-box {
            padding: 18px 20px;
        }
        
        .chat-message-user,
        .chat-message-bot,
        .chat-message-blocked,
        .chat-message-compliance {
            margin-left: 20px;
            margin-right: 20px;
        }
        
        .input-container {
            padding: 18px;
        }
        
        .footer-box {
            padding: 16px 18px;
        }
    }
    
    /* FIX: Force Input and Button to same height and alignment */
    div.stButton > button {
        height: 52px; /* Matches standard Streamlit input height */
        padding-top: 0;
        padding-bottom: 0;
        margin-top: 0px !important; /* Remove default margin */
        line-height: normal; /* Center text vertically */
        border: 2px solid #3B82F6; /* Match input border width */
        white-space: nowrap; /* Prevent text from wrapping vertically */
        padding-left: 20px;
        padding-right: 20px;
    }
    
    /* Remove the default label margin from the button column to align with input */
    div[data-testid="column"]:nth-of-type(2) .stButton {
        margin-top: 29px; /* This aligns with the input field which has a hidden label */
    }
    
    /* Ensure API config button in sidebar is visible */
    [data-testid="stSidebar"] div.stButton > button {
        height: auto; /* Let sidebar button size naturally */
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# HEADER SECTION - Premium Card with Title and Subtitle
# --------------------------------------------------------------------------
st.markdown("""
<div class="header-card">
    <div class="header-title">
        ⚖️ AI-Powered Guide to Understanding Court Procedures
    </div>
    <div class="header-subtitle">
        A public-facing educational assistant for explaining judicial processes
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# LEGAL NOTICE BOX - High Visibility Warning with Exact Wording
# --------------------------------------------------------------------------
st.markdown("""
<div class="legal-notice-box">
    <div class="legal-notice-title">
        ⚠️ IMPORTANT LEGAL NOTICE
    </div>
    <div class="legal-notice-text">
        This tool is designed exclusively for <strong>educational purposes</strong> to explain general court procedures.<br><br>
        <strong>This system does NOT:</strong><br>
        ❌ Provide legal advice or recommendations<br>
        ❌ Analyze specific cases or predict outcomes<br>
        ❌ Replace consultation with a qualified legal professional<br><br>
        <strong>For legal assistance, please consult a licensed attorney.</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# API KEY CONFIGURATION (Above Chat)
# --------------------------------------------------------------------------
# Initialize session state for API key visibility
if 'show_api_key_input' not in st.session_state:
    st.session_state.show_api_key_input = False

col_api_1, col_api_2 = st.columns([4, 1])
with col_api_2:
    # Toggle button to show/hide input
    if st.button("🔑 Configure API Key", key="api_config_btn", help="Set your Gemini API Key"):
        st.session_state.show_api_key_input = not st.session_state.show_api_key_input

# Show input only if toggled on
if st.session_state.show_api_key_input:
    with st.container():
        st.markdown('<div style="background: #F3F4F6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">', unsafe_allow_html=True)
        with st.form("api_key_form"):
            key_input = st.text_input(
                "Enter Gemini API Key", 
                type="password",
                help="Your key is used only for this session."
            )
            submitted = st.form_submit_button("Save Key")
            if submitted:
                st.session_state.user_api_key = key_input
                st.success("API Key saved!")
                st.session_state.show_api_key_input = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Init user_api_key in session state if not present (to avoid NameError in main loop)
if 'user_api_key' not in st.session_state:
    st.session_state.user_api_key = None

# --------------------------------------------------------------------------
# CHAT HISTORY DISPLAY - Scrollable with Message Bubbles
# --------------------------------------------------------------------------
def display_chat_history():
    """Display chat history with user and bot message bubbles"""
    if len(st.session_state.chat_history) == 0:
        st.markdown("""
<div class="chat-history-container">
    <div class="empty-state">
        <div class="empty-state-icon">💬</div>
        <div class="empty-state-text">No messages yet. Ask a question to get started!</div>
    </div>
</div>
""", unsafe_allow_html=True)
    else:
        chat_html = '<div class="chat-history-container">'
        
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                chat_html += f"""
<div class="chat-message-user">
    <div class="chat-message-user-label">You asked:</div>
    <div class="chat-message-user-text">{msg['message']}</div>
</div>
"""
            elif msg['role'] == 'bot':
                if msg['type'] == 'blocked':
                    chat_html += f"""
<div class="chat-message-blocked">
    <div class="chat-message-bot-label">🚫 Request Blocked</div>
    <div class="chat-message-bot-text">{msg['message']}</div>
</div>
"""
                elif msg['type'] == 'compliance':
                    chat_html += f"""
<div class="chat-message-compliance">
    <div class="chat-message-bot-label">🛑 Compliance Alert</div>
    <div class="chat-message-bot-text">{msg['message']}</div>
</div>
"""
                else:  # success
                    chat_html += f"""
<div class="chat-message-bot">
    <div class="chat-message-bot-label">⚖️ Judicial Assistant</div>
    <div class="chat-message-bot-text">{msg['message']}</div>
</div>
"""
        
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

# Display chat history
display_chat_history()


# --------------------------------------------------------------------------
# INPUT BAR - Inline Layout with Button
# --------------------------------------------------------------------------
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Create columns for inline layout
# Giving button significantly more space (25% of width) to prevent wrapping
col1, col2 = st.columns([3, 1])

with col1:
    # Text Input with hidden label
    # The 'label_visibility="visible"' but with empty string often aligns better than "collapsed"
    # because "collapsed" removes the space where the label would be, executing alignment issues.
    # However, since we used CSS to add top margin to the button, we keep this "collapsed".
    user_query = st.text_input(
        "Ask Your Question",
        placeholder="Example: Explain court case filing process | What is a summons?",
        max_chars=300,
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    # The CSS rule `div[data-testid="column"]:nth-of-type(2) .stButton { margin-top: 29px; }`
    # handles the alignment down to match the input box.
    submit_clicked = st.button("🔍 Explain", key="submit_btn")

if submit_clicked:
    if not user_query.strip():
        st.warning("⚠️ Please enter a question to continue.")
    else:
        with st.spinner("🔄 Analyzing your question..."):
            # Add user message to chat history (UI only)
            st.session_state.chat_history.append({
                'role': 'user',
                'message': user_query,
                'type': 'user'
            })
            
            # LAYER 1: INPUT INTENT FILTER
            if not IntentFilter.is_safe(user_query):
                # Add blocked response to chat history
                st.session_state.chat_history.append({
                    'role': 'bot',
                    'message': IntentFilter.get_refusal_message(),
                    'type': 'blocked'
                })
            else:
                # LAYER 2: AI ENGINE (stateless - no history passed)
                # Pass the user_api_key from session state if provided
                api_key_to_use = st.session_state.user_api_key
                raw_response = AIEngine.get_explanation(user_query, api_key=api_key_to_use)
                
                # LAYER 3: RESPONSE GUARD
                final_response = ResponseGuard.validate_output(raw_response)
                
                if final_response == ResponseGuard.BLOCK_MESSAGE:
                    # Add compliance alert to chat history
                    st.session_state.chat_history.append({
                        'role': 'bot',
                        'message': final_response,
                        'type': 'compliance'
                    })
                else:
                    # Add success response to chat history
                    st.session_state.chat_history.append({
                        'role': 'bot',
                        'message': final_response,
                        'type': 'success'
                    })
        
        # Rerun to display updated chat history
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# FOOTER SECTION - Subtle Disclaimer and Credits
# --------------------------------------------------------------------------
st.markdown("""
<div class="footer-box">
    <div class="footer-disclaimer">
        This application provides procedural education only and does not offer legal advice.
    </div>
    <div class="footer-credits">
        Built for public legal awareness using responsible AI principles
    </div>
</div>
""", unsafe_allow_html=True)
