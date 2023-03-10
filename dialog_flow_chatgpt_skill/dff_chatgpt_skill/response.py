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
    msg_text = (
        "We registered your transaction. "
        + f"Requested titles are: {', '.join(ctx.misc[utils.SLOTS]['items'])}. "
        + f"Delivery method: {ctx.misc[utils.SLOTS]['delivery']}. "
        + f"Payment method: {ctx.misc[utils.SLOTS]['payment_method']}. "
        + "Type `abort` to cancel, type `ok` to continue."
    )
    msg = Message(text=msg_text)
    return msg
