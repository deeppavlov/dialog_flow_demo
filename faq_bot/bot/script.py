from dff.script import RESPONSE, TRANSITIONS, Context, Actor, LOCAL
import dff.script.conditions as cnd
from dff.script.core.message import Button
from dff.messengers.telegram import TelegramMessage, TelegramUI, CallbackQuery, ParseMode
from .model import faq


def suggest_similar_questions(ctx: Context, actor: Actor):
    if ctx.validation:
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
            text="I don't have an answer to that question. Here's a list of questions I know an answer to:",
            ui=TelegramUI(
                buttons=[
                    Button(text=q, payload=q) for q in faq
                ]
            )
        )
    else:
        return TelegramMessage(
            text="I found similar questions in my database:",
            ui=TelegramUI(
                buttons=[
                    Button(text=q, payload=q) for q in similar_questions
                ]
            )
        )


def answer_question(ctx: Context, actor: Actor):
    if ctx.validation:
        return TelegramMessage()
    last_request = ctx.last_request
    if last_request is None:
        raise RuntimeError("No last requests.")
    if last_request.commands is None:
        raise RuntimeError("No commands")
    if len(last_request.commands) != 1:
        raise RuntimeError("Number of Commands != 1")
    command = last_request.commands[0]
    if not isinstance(command, CallbackQuery):
        raise RuntimeError(type(command))
    return TelegramMessage(text=faq[command.data], parse_mode=ParseMode.HTML)


qa_transitions = {
    ("qa_flow", "suggest_questions"): lambda ctx, actor: ctx.last_request.text is not None,
    ("qa_flow", "answer_question"): lambda ctx, actor: ctx.last_request.commands is not None,
}


script = {
    "proxy_flow": {
        "start_node": {
            RESPONSE: TelegramMessage(),
            TRANSITIONS: {
                "welcome_node": cnd.exact_match(TelegramMessage(text="/start"))
            }
        },
        "welcome_node": {
            RESPONSE: TelegramMessage(text="Welcome! Ask me questions about Arch Linux."),
            TRANSITIONS: qa_transitions
        },
        "fallback_node": {
            RESPONSE: TelegramMessage(text="Something went wrong. Use `/restart` to start over."),
            TRANSITIONS: {
                "welcome_node": cnd.exact_match(TelegramMessage(text="/restart"))
            }
        }
    },
    "qa_flow": {
        LOCAL: {
            TRANSITIONS: qa_transitions,
        },
        "suggest_questions": {
            RESPONSE: suggest_similar_questions,
        },
        "answer_question": {
            RESPONSE: answer_question,
        }
    },
}
