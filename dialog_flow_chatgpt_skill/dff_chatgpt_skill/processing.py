import re

from dff.script import Context, Actor
from pyChatGPT import ChatGPT
from . import utils

CONFIG = utils.get_config()


def extract_intents():
    def extract_intents_inner(ctx: Context, actor: Actor) -> Context:
        ctx.misc[utils.DNNC_INTENTS] = []
        return ctx

    return extract_intents_inner


def generate_response():
    expression = re.compile(r"true", re.IGNORECASE)
    def generate_response_inner(ctx: Context, actor: Actor) -> Context:
        if ctx.validation:
            return ctx

        chatgpt_api = ChatGPT(**CONFIG)
        text = ctx.last_request.text
        full_prompt = [utils.CHATGPT_MAIN_PROMPT, text]
        chatgpt_output = chatgpt_api.send_message(full_prompt).get("message", "")
        full_coherence_prompt = [utils.CHATGPT_COHERENCE_PROMPT, text, chatgpt_output]
        coherence_output = chatgpt_api.send_message(full_coherence_prompt).get("message", "")
        ctx.misc[utils.CHATGPT_OUTPUT] = chatgpt_output
        ctx.misc[utils.CHATGPT_COHERENCE] = True if re.search(expression, coherence_output) else False
        return ctx

    return generate_response_inner


def extract_item():
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
    expression = re.compile(r"(card|cash)")
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
    expression = re.compile(r"(pickup|home)")
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
