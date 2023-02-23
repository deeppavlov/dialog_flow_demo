from dff.script import Context, Actor, Message

from . import utils


def choose_response(ctx: Context, _: Actor) -> Message:
    """
    Return ChatGPT response if it is coherent, fall back to
    predetermined response otherwise.
    """
    if ctx.validation:
        return Message()
    coherence = ctx.misc[utils.CHATGPT_COHERENCE]
    response = ctx.misc[utils.CHATGPT_OUTPUT]
    return Message(text=(response if coherence else utils.FALLBACK_RESPONSE))


def confirm(ctx: Context, _: Actor) -> Message:
    if ctx.validation:
        return Message()
msg = Message(
        text="We registered your transaction. Requested titles are: {}. Type anything to continue...".format(
            ", ".join(ctx.misc[utils.SLOTS]["items"])
        )
    )
    return msg
