import google.generativeai as genai
from config import Config


class AIEngine:
    """
    Security Layer 2: The Core AI Engine.
    
    Responsibilities:
    1. Authenticate with Google AI Studio.
    2. Enforce the IMMUTABLE System Prompt.
    3. Generate responses using the specified Gemini model.
    """

    # ---------------------------------------------------------
    # COMPLIANCE CRITICAL: IMMUTABLE SYSTEM PROMPT
    # This prompt is hardcoded and cannot be bypassed via UI.
    # ---------------------------------------------------------
    _SYSTEM_PROMPT = """
You are a Judicial Court Process Explainer Bot.

Your role is strictly limited to explaining general court procedures,
case flow stages, hearing processes, and common judicial terms
in a neutral, informational, and non-advisory manner.

You must NOT:
- Provide legal advice or recommendations
- Analyze or comment on specific cases
- Predict outcomes, judgments, or punishments
- Interpret laws for personal situations
- Suggest actions or strategies
- Express opinions or conclusions

You must:
- Explain processes at a high level
- Use simple, neutral language
- Avoid directive words such as "should", "must", or "best"
- Clearly stay within procedural explanations only

If a user asks for legal advice, opinions, or case-specific guidance,
politely refuse and offer a general explanation of the court process instead.

Your responses must always reflect public legal awareness,
not legal assistance.
"""
    # ---------------------------------------------------------

    @staticmethod
    def configure(api_key=None):
        """Configures the GenAI library with the API key."""
        # Use provided key or fallback to config
        key_to_use = api_key if api_key else Config.GOOGLE_API_KEY
        
        if not key_to_use:
            return False
            
        genai.configure(api_key=key_to_use)
        return True

    @staticmethod
    def get_explanation(user_query: str, api_key=None) -> str:
        """
        Sends the user query to the Gemini model with the strict system prompt.
        
        Args:
            user_query: The sanitized user input.
            api_key: Optional API key provided by user.
            
        Returns:
            The model's textual response.
        """
        if not AIEngine.configure(api_key):
            return "System Error: API Configuration Missing. Please provide an API Key in the settings or check server logs."

        try:
            model = genai.GenerativeModel(
                model_name=Config.MODEL_NAME,
                system_instruction=AIEngine._SYSTEM_PROMPT
            )

            generation_config = genai.GenerationConfig(
                temperature=0.3,
                max_output_tokens=1000,
            )

            response = model.generate_content(
                user_query,
                generation_config=generation_config
            )

            # Handle response properly
            if response and response.text:
                return response.text
            elif response and hasattr(response, 'candidates') and response.candidates:
                return response.candidates[0].content.parts[0].text
            else:
                return "The AI model did not return a valid response. Please try again."

        except Exception as e:
            error_msg = str(e)
            if "API_KEY" in error_msg or "invalid" in error_msg.lower():
                return "⚠️ API Key Error: Please verify your GOOGLE_API_KEY is set correctly in the .env file."
            elif "quota" in error_msg.lower():
                return "⚠️ API Quota Exceeded: Please check your Google AI API usage limits."
            elif "not found" in error_msg.lower() or "model" in error_msg.lower():
                return f"⚠️ Model Error: The model '{Config.MODEL_NAME}' may not be available. Please verify the model name."
            else:
                return f"⚠️ An error occurred: {error_msg}"
