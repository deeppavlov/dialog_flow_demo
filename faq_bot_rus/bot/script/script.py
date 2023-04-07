"""
Script
------
This module defines a script that the bot follows during conversation.
"""
from dff.script import RESPONSE, TRANSITIONS, LOCAL
import dff.script.conditions as cnd
from dff.messengers.telegram import TelegramMessage

from .responses import answer_question, suggest_similar_questions
from .conditions import received_button_click, received_text

qa_transitions = {
    ("qa_flow", "suggest_questions"): received_text,
    ("qa_flow", "answer_question"): received_button_click,
}

script = {
    "proxy_flow": {
        "start_node": {
            RESPONSE: TelegramMessage(),
            TRANSITIONS: {"welcome_node": cnd.exact_match(TelegramMessage(text="/start"))},
        },
        "welcome_node": {
            RESPONSE: TelegramMessage(text="Добро пожаловать! Задайте мне вопросы об Arch Linux."),
            TRANSITIONS: qa_transitions,
        },
        "fallback_node": {
            RESPONSE: TelegramMessage(text="Что-то пошло не так. Используйте `/restart`, чтобы начать с начала."),
            TRANSITIONS: {"welcome_node": cnd.exact_match(TelegramMessage(text="/restart"))},
        },
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
        },
    },
}
