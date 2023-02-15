"""
Transitions
-----------
This module defines transitions between nodes and conditions of those transitions.
"""
from typing import cast

from dff.script import Context, Actor
from dff.messengers.telegram import TelegramMessage


def received_text(ctx: Context, _: Actor):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request

    return last_request.text is not None


def received_button_click(ctx: Context, _: Actor):
    """Return true if the last update from user is a button press."""
    if ctx.validation:  # Regular `Message` doesn't have `callback_query` field, so this fails during validation
        return False
    last_request = cast(TelegramMessage, ctx.last_request)

    return last_request.callback_query is not None


qa_transitions = {
    ("qa_flow", "suggest_questions"): received_text,
    ("qa_flow", "answer_question"): received_button_click,
}
