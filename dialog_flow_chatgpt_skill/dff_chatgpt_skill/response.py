from dff.script import Context, Actor, Message

from . import utils

def choose_response(ctx: Context, actor: Actor) -> Message:
    if ctx.validation:
        return Message()
    coherence = ctx.misc[utils.CHATGPT_COHERENCE]
    response = ctx.misc[utils.CHATGPT_OUTPUT]
    return Message(text=(response if coherence else utils.FALLBACK_RESPONSE))