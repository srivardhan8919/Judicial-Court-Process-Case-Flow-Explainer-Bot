import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Central configuration for the application.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = "gemini-3-flash-preview"
    APP_TITLE = "Judicial Court Process Explainer"
    DISCLAIMER = "This tool explains general court procedures. It does not provide legal advice."
