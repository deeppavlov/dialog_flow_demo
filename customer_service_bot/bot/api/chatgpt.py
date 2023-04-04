import os
import openai

CHATGPT_MAIN_PROMPT = """
"You are an assistant for a book shop with the following description. 
Book Lovers Paradise" is a one-stop destination for all things literary
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
"""

CHATGPT_QUESTION_PROMPT = """
What follows is a user query: answer if related to the given description or deny if unrelated.
"""

CHATGPT_COHERENCE_PROMPT = """
What follows is a question and an answer. Just write 'true' if the answer was satisfactory or 'false' otherwise. 
"""

openai.api_key = os.getenv("OPENAI_API_TOKEN")


def get_output(request: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": CHATGPT_MAIN_PROMPT},
            {"role": "system", "content": CHATGPT_QUESTION_PROMPT},
            {"role": "user", "content": request}
        ]
    )
    return response['choices'][0]['message']['content']


def get_coherence(request: str, response: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": CHATGPT_MAIN_PROMPT},
            {"role": "system", "content": CHATGPT_COHERENCE_PROMPT},
            {"role": "user", "content": request},
            {"role": "assistant", "content": response}
        ]
    )
    return response['choices'][0]['message']['content']
