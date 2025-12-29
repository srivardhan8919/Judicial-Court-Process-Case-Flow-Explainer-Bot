import re

class ResponseGuard:
    """
    Security Layer 3: Output Compliance Check.

    This layer runs AFTER the LLM.
    It blocks only USER-DIRECTED advice, judgments, or recommendations,
    while allowing neutral, institutional, and procedural explanations.

    Governance Principle:
    - Words like "should" or "must" are NOT dangerous by themselves
    - They are dangerous ONLY when directed at the user
    """

    # ❌ Block ONLY user-directed or advisory language
    FORBIDDEN_TERMS = [
        # User-directed advice
        r"\byou\s+should\b",
        r"\byou\s+must\b",
        r"\bone\s+should\b",
        r"\ba\s+person\s+should\b",
        r"\byou\s+need\s+to\b",

        # Explicit recommendations
        r"\bi\s+recommend\b",
        r"\bwe\s+recommend\b",
        r"\bbest\s+option\b",
        r"\bbest\s+way\b",

        # Outcome / legal judgment phrasing
        r"\blegal\s+judgment\b",
        r"\bis\s+illegal\b",
        r"\bare\s+illegal\b"
    ]

    # ✅ Explicit refusal detection
    # Any refusal is treated as BLOCKED_OUTPUT for governance/testing
    REFUSAL_PATTERNS = [
        r"\bi\s+cannot\b",
        r"\bi\s+can't\b",
        r"\bi\s+am\s+unable\b",
        r"\bnot\s+able\s+to\s+provide\b",
        r"\bstrictly\s+limited\b",
        r"\bi\s+do\s+not\s+provide\b",
        r"\brefuse\b"
    ]

    BLOCK_MESSAGE = (
        "Compliance Alert: The generated response was blocked because it contained "
        "language that may be interpreted as advisory or judgmental. "
        "This bot is strictly for educational procedural explanations only. "
        "Please ask for a general process overview."
    )

    @staticmethod
    def validate_output(llm_response: str) -> str:
        """
        Validates the LLM response.

        Returns:
        - BLOCK_MESSAGE if unsafe
        - Original response if compliant
        """

        if not llm_response:
            return llm_response

        response_lower = llm_response.lower()

        # 1️⃣ Explicit refusal → classify as BLOCKED_OUTPUT
        for pattern in ResponseGuard.REFUSAL_PATTERNS:
            if re.search(pattern, response_lower):
                return ResponseGuard.BLOCK_MESSAGE

        # 2️⃣ User-directed advisory language → BLOCK
        for pattern in ResponseGuard.FORBIDDEN_TERMS:
            if re.search(pattern, response_lower):
                return ResponseGuard.BLOCK_MESSAGE

        # 3️⃣ Otherwise safe
        return llm_response
