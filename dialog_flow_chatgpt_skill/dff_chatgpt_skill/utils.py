import os
from typing import Optional


def get_config(email: Optional[str] = None, password: Optional[str] = None):
    true_email = email or os.getenv("OPENAI_API_LOGIN")
    true_password = password or os.getenv("OPENAI_API_PASSWORD")
    if not true_email:
        raise OSError("Openai API login missing.")
    if not true_password:
        raise OSError("Openai API password missing.")
    return {
        "auth_type": "google",
        "email": true_email,
        "password": true_password
    }


SLOTS = "slots"
DNNC_INTENTS = "dnnc_intents"
CHATGPT_OUTPUT = "chatgpt_output"
CHATGPT_COHERENCE = "chatgpt_coherence"
DNNC_URL = "http://localhost:4999/respond"

CHATGPT_MAIN_PROMPT = """
"Book Lovers Paradise" is a one-stop destination for all things literary
Located in the heart of the city at 123 Main Street
Open seven days a week, from 9 AM to 9 PM
Extensive collection of genres, including fiction, non-fiction, children's books, cookbooks, self-help books and more
Knowledgeable staff to help you find the perfect read
Wide range of unique and rare books for collectors
Online catalogue for easy browsing and ordering
Comfortable seating areas and peaceful atmosphere for a perfect escape
Customer satisfaction is a top priority
Generous refund policy within 30 days of purchase
Loyalty program for frequent customers
Members receive 10% off every purchase and access to special sales and promotions.
What follows is a user query: answer it if it is related to the given description or deny it if it is unrelated.
"""

CHATGPT_COHERENCE_PROMPT = """
What follows is a question and an answer. Just write 'true' if the answer was satisfactory or 'false' otherwise. 
"""
