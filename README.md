# ⚖️ Judicial Court Process Explainer Bot

A **premium, AI-powered educational tool** designed to explain general court procedures, case flows, and judicial terminology to the public. Built with **Streamlit** and **Google Gemini AI**, this application prioritizes visual excellence, educational clarity, and strict safety compliance.

---

## 🌟 Key Features

### 🎨 Premium UI/UX
- **Modern Light Theme**: sleek, calm, and trustworthy design with rounded cards and soft shadows.
- **Interactive Chat Interface**: Clean message bubbles with clear distinction between user queries and AI responses.
- **Responsive Layout**: Optimized for desktop and mobile viewing with a "Get Explanation" button that fits perfectly on any screen.

### 🛡️ Safety & Compliance (Governance)
This bot is engineered with a **multi-layer safety architecture** to prevent legal liability:
1.  **Strict Intent Filtering**: Blocks non-procedural queries (e.g., "Should I sue?", "Is he guilty?").
2.  **Immutable System Prompt**: Enforces a neutral, educational persona that *never* gives legal advice.
3.  **Response Guardrails**: Validates every AI output to ensure no advisory language ("you should", "must") leaks through.
4.  **Prominent Disclaimers**: Mandatory legal notice headers and footers on every screen.

### ⚙️ Dynamic Configuration
- **Visual API Key Manager**: Users can securely enter their own Gemini API key directly in the UI for the session.
- **Environment Fallback**: Automatically uses the `.env` key if no custom key is provided.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python) + Custom CSS
- **AI Engine**: Google Gemini (via `google-generativeai`)
- **Language**: Python 3.10+
- **Configuration**: `python-dotenv`

---

## 🚀 Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/judicial-explainer-bot.git
    cd judicial-explainer-bot
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```ini
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

5.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

---

## 📂 Project Structure

```text
judicial-explainer-bot/
├── app.py                  # Main Streamlit frontend application
├── ai_engine.py            # Core AI logic (Gemini integration + System Prompt)
├── intent_filter.py        # Layer 1: Input safety validation
├── response_guard.py       # Layer 3: Output compliance verification
├── config.py               # Central configuration settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API Key)
└── .streamlit/
    └── config.toml         # Streamlit theme configuration (Forces Light Mode)
```

---

## 📝 Usage Guide

1.  **Asking Questions**: Type any procedural question into the input bar (e.g., *"What is a summons?"* or *"Explain the steps of a civil trial"*).
2.  **API Key**: purely optional. If you have an API key in your `.env` file, it works automatically. If you want to use a different key, click **"🔑 Configure API Key"** above the chat window.
3.  **Safety Blocks**: If you ask for legal advice (e.g., *"My neighbor hit my car, what should I do?"*), the bot will politely refuse and explain its educational limitations.

---

## ⚠️ Legal Disclaimer

**This tool is for educational purposes only.**

It does **NOT**:
- Provide legal advice or recommendations.
- Analyze specific cases.
- Replace consultation with a qualified attorney.

*Built for public legal awareness using responsible AI principles.*
