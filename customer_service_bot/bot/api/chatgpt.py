"""
ChatGPT
-------
This module defines functions for OpenAI API interaction.
"""
from langchain.llms import OpenAI
import langchain
from langchain.cache import InMemoryCache

CHATGPT_MAIN_PROMPT = """
You are a helpful assistant for a book shop "Book Lovers Paradise".
Located at 123 Main Street.
Open seven days a week, from 9 AM to 9 PM.
Extensive collection of genres, including fiction, and non-fiction.
Knowledgeable staff. Online catalogue for easy browsing and ordering.
Comfortable seating areas and peaceful atmosphere.
Refund policy within 30 days of purchase.
Loyalty program for frequent customers (10% off purchases).
"""  # shortened the prompt to reduce token consumption.

CHATGPT_QUESTION_PROMPT = langchain.PromptTemplate(
    input_variables=["question"],
    template=CHATGPT_MAIN_PROMPT
    + """

    What follows is a user query: 
    answer if related to the given description or deny if unrelated.
    {question}
    """,
)

CHATGPT_COHERENCE_PROMPT = langchain.PromptTemplate(
    input_variables=["question", "answer"],
    template=CHATGPT_MAIN_PROMPT
    + """

    What follows is a question and an answer. 
    Just write 'true' if the answer was satisfactory or 'false' otherwise. 
    {question} 
    {answer}
    """,
)

langchain.llm_cache = InMemoryCache()
llm = OpenAI(model_name="gpt-3.5-turbo", cache=True)


def get_output_factory():
    """
    Construct a get_output function encapsulating the execution counter.
    The function prompts ChatGPT for generated output.
    The main prompt is only included
    on the first invocation of the function.
    """
    llm_chain = langchain.LLMChain(prompt=CHATGPT_QUESTION_PROMPT, llm=llm)

    def get_output_inner(request: str) -> str:
        result = llm_chain.run(request)
        return result

    return get_output_inner


def get_coherence_factory():
    llm_chain = langchain.LLMChain(prompt=CHATGPT_COHERENCE_PROMPT, llm=llm)

    def get_coherence(request: str, response: str) -> str:
        """
        Prompt ChatGPT to evaluate the coherence of a request
        response pair.
        """
        result = llm_chain.run(question=request, answer=response)
        return result

    return get_coherence


get_output = get_output_factory()
