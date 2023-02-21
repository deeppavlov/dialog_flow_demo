import re
import requests
from dff.script import Context, Actor
from revChatGPT.V1 import Chatbot
from . import utils

CONFIG = utils.get_config()


def send_message(bot: Chatbot, message: str) -> str:
    """
    Make a request to ChatGPT API.
    """
    responses = []
    for data in bot.ask(message, conversation_id=bot.config.get("conversation"), parent_id=bot.config.get("parent_id")):
        responses.append(data["message"])
    if len(responses) > 0:
        return responses[-1]
    return ""


def extract_intents():
    """
    Extract intents from DNNC response.
    """

    def extract_intents_inner(ctx: Context, actor: Actor) -> Context:
        request_body = {"dialog_contexts": [ctx.last_request.text]}
        try:
            response = requests.post(utils.DNNC_URL, json=request_body)
        except requests.RequestException:
            response = None
        ctx.misc[utils.DNNC_INTENTS] = [response.json()[0][0]] if response and response.status_code == 200 else []
        return ctx

    return extract_intents_inner


def clear_intents():
    """
    Clear intents container.
    """

    def clear_intents_inner(ctx: Context, actor: Actor) -> Context:
        ctx.misc[utils.DNNC_INTENTS] = []
        return ctx

    return clear_intents_inner


def clear_slots():
    """
    Clear slots container.
    """

    def clear_slots_inner(ctx: Context, actor: Actor) -> Context:
        ctx.misc[utils.SLOTS] = {}
        return ctx

    return clear_slots_inner


def generate_response():
    """
    Store ChatGPT output and ChatGPT coherence measure in the context.
    """
    expression = re.compile(r"true", re.IGNORECASE)

    def generate_response_inner(ctx: Context, actor: Actor) -> Context:
        if ctx.validation:
            return ctx

        bot = Chatbot(config=CONFIG)
        text = ctx.last_request.text
        full_prompt = " ".join([utils.CHATGPT_MAIN_PROMPT, text])
        chatgpt_output = send_message(bot, full_prompt)
        full_coherence_prompt = " ".join([utils.CHATGPT_COHERENCE_PROMPT, text, chatgpt_output])
        coherence_output = send_message(bot, full_coherence_prompt)
        ctx.misc[utils.CHATGPT_OUTPUT] = chatgpt_output
        ctx.misc[utils.CHATGPT_COHERENCE] = True if re.search(expression, coherence_output) else False
        return ctx

    return generate_response_inner


def extract_item():
    """
    Extract item slot.
    """
    expression = re.compile(r".+")

    def extract_item_inner(ctx: Context, actor: Actor) -> Context:
        if ctx.validation:
            return ctx

        text: str = ctx.last_request.text
        search = re.search(expression, text)
        if search is not None:
            group = search.group()
            ctx.misc[utils.SLOTS]["items"] = group.split(", ")
        return ctx

    return extract_item_inner


def extract_payment_method():
    """Extract payment method slot."""
    expression = re.compile(r"(card|cash)", re.IGNORECASE)

    def extract_payment_method_inner(ctx: Context, actor: Actor) -> Context:
        if ctx.validation:
            return ctx

        text: str = ctx.last_request.text
        search = re.search(expression, text)
        if search is not None:
            ctx.misc[utils.SLOTS]["payment_method"] = search.group()
        return ctx

    return extract_payment_method_inner


def extract_delivery():
    """
    Extract delivery slot.
    """
    expression = re.compile(r"(pickup|deliver)", re.IGNORECASE)

    def extract_delivery_inner(ctx: Context, actor: Actor) -> Context:
        if ctx.validation:
            return ctx

        text: str = ctx.last_request.text
        search = re.search(expression, text)
        if search is not None:
            ctx.misc[utils.SLOTS]["delivery"] = search.group()
        return ctx

    return extract_delivery_inner


def extract_address():
    """
    Extract address slot.
    """
    expression = re.compile(r".+")

    def extract_address_inner(ctx: Context, actor: Actor) -> Context:
        if ctx.validation:
            return ctx

        text: str = ctx.last_request.text
        search = re.search(expression, text)
        if search is not None:
            ctx.misc[utils.SLOTS]["address"] = search.group()
        return ctx

    return extract_address_inner
