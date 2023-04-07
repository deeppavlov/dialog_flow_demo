"""
Responses
---------
This module defines different responses the bot gives.
"""
from typing import cast

from dff.script import Context, Actor
from dff.script.core.message import Button
from dff.messengers.telegram import TelegramMessage, TelegramUI, ParseMode
from ..model import faq


def suggest_similar_questions(ctx: Context, _: Actor):
    """Suggest questions similar to user's query by showing buttons with those questions."""
    if ctx.validation:  # this function requires non-empty fields and cannot be used during script validation
        return TelegramMessage()
    last_request = ctx.last_request
    if last_request is None:
        raise RuntimeError("No last requests.")
    if last_request.annotations is None:
        raise RuntimeError("No annotations.")
    similar_questions = last_request.annotations.get("similar_questions")
    if similar_questions is None:
        raise RuntimeError("Last request has no text.")

    if len(similar_questions) == 0:  # question is not similar to any questions
        return TelegramMessage(
            text="У меня нет ответа на этот вопрос. Вот список вопросов, на которые я могу дать ответ:",
            ui=TelegramUI(buttons=[Button(text=q, payload=q) for q in faq]),
        )
    else:
        return TelegramMessage(
            text="Я нашел похожие вопросы в своей базе данных:",
            ui=TelegramUI(buttons=[Button(text=q, payload=q) for q in similar_questions]),
        )


def answer_question(ctx: Context, _: Actor):
    """Answer a question asked by a user by pressing a button."""
    if ctx.validation:  # this function requires non-empty fields and cannot be used during script validation
        return TelegramMessage()
    last_request = ctx.last_request
    if last_request is None:
        raise RuntimeError("No last requests.")
    last_request = cast(TelegramMessage, last_request)
    if last_request.callback_query is None:
        raise RuntimeError("No callback query")

    return TelegramMessage(text=faq[last_request.callback_query], parse_mode=ParseMode.HTML)
