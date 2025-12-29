import re

class IntentFilter:
    """
    Security Layer 1: Input Intent Filtering.
    
    This layer sits BEFORE the LLM. It intercepts and blocks user queries 
    that violate the strict boundaries of the application.
    
    BLOCKED INTENTS:
    - Legal advice ("What should I do?")
    - Outcome prediction ("Will I win?")
    - Personal case analysis ("My case details are...")
    - Judgments on legality ("Is this illegal?")
    - Strategy/Defense ("How to defend...")
    """

    # Compiled regex patterns for forbidden intents
    FORBIDDEN_PATTERNS = [
        # A. ADVICE
        r"what\s+should\s+i\s+do",
        r"should\s+i",
        r"do\s+you\s+recommend",
        r"can\s+you\s+recommend",
        r"advice\s+on",
        r"give\s+me\s+advice",
        r"best\s+course\s+of\s+action",
        r"best\s+way\s+to\s+win",
        r"how\s+should\s+i",

        # B. OUTCOME PREDICTION
        r"will\s+i\s+win",
        r"chances\s+of\s+winning",
        r"will\s+the\s+judge",
        r"rule\s+in\s+my\s+favor",
        r"what\s+will\s+happen",
        r"sentence\s+will\s+be",
        r"what\s+punishment",
        r"case\s+.*dismissed", # Matches "case be dismissed"
        r"likely\s+outcome",
        r"predict\s+my",
        r"probability\s+of",
        r"how\s+long\s+until.*justice", # Specific check

        # C. STRATEGY / MANIPULATION
        r"influence\s+a\s+judge",
        r"favorable\s+verdict",
        r"make\s+my\s+case\s+stronger",
        r"avoid\s+punishment",
        r"beat\s+the\s+charge",
        r"loophole",
        r"get\s+off\s+easy",
        r"how\s+to\s+defend",
        r"best\s+strategy",
        r"delay\s+.*case",

        # D. ROLE PLAYING
        r"act\s+like\s+my\s+lawyer",
        r"act\s+as\s+my\s+lawyer",
        r"what\s+would\s+a\s+lawyer\s+say",
        r"advice\s+.*lawyer",
        r"as\s+a\s+judge",
        r"pretend\s+you\s+are",
        
        # E. CASE SPECIFIC / LEGALITY JUDGMENTS
        r"my\s+case", # Block "my case" broadly to prevent personal analysis
        r"find\s+a\s+lawyer",
        r"is\s+this\s+legal",
        r"is\s+this\s+illegal",
        r"is\s+it\s+illegal",
        r"is\s+my\s+action\s+legal",
        r"can\s+i\s+win",

        # F. AMBIGUOUS CIVIC / CONSEQUENCES
        r"not\s+appear\s+in\s+court",
        r"ignoring\s+.*court\s+notice",
        r"non-compliance",
        r"do\s+not\s+cooperate",
        r"what\s+happens\s+if\s+ignored",
        
        # G. GLENERIC PERSON TRICK / TIME / AUTHORITY
        r"should\s+a\s+person",
        r"should\s+an\s+accused",
        r"should\s+a\s+defendant",
        r"how\s+long\s+does",
        r"how\s+much\s+time",
        r"how\s+fast\s+are",
        r"must\s+it\s+be\s+followed",
        r"are\s+.*compulsory",
        
        # H. HYPOTHETICAL / MORAL / THIRD PERSON
        r"just\s+for\s+learning",
        r"only\s+academic",
        r"hypothetically",
        r"my\s+friend",
        r"someone\s+i\s+know",
        r"is\s+it\s+fair",
        r"is\s+it\s+right",
        r"unethical",
        
        # I. LAW INTERPRETATION
        r"law\s+say\s+about",
        r"punishment\s+for",
        r"penalties\s+defined"
    ]

    REFUSAL_MESSAGE = (
        "I can’t help with advice or opinions on specific legal matters.\n"
        "However, I can explain the general court process or procedures "
        "if that would be useful."
    )

    @staticmethod
    def is_safe(user_query: str) -> bool:
        """
        Checks if the user query contains forbidden patterns.
        Returns True if safe, False if blocked.
        """
        # Normalize: lowercase for case-insensitive matching
        query_lower = user_query.lower()

        for pattern in IntentFilter.FORBIDDEN_PATTERNS:
            if re.search(pattern, query_lower):
                return False
        
        return True

    @staticmethod
    def get_refusal_message() -> str:
        """Returns the standardized refusal message."""
        return IntentFilter.REFUSAL_MESSAGE
