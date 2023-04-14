import pytest
from dff.utils.testing.common import check_happy_path
from dff.messengers.telegram import TelegramMessage, TelegramUI
from dff.script import RESPONSE
from dff.script.core.message import Button

from bot.script.script import script
from bot.bot import pipeline
from bot.model import faq


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "happy_path",
    [
        (
            (TelegramMessage(text="/start"), script["proxy_flow"]["welcome_node"][RESPONSE]),
            (
                TelegramMessage(text="Зачем мне использовать Arch?"),
                TelegramMessage(
                    text="Я нашел похожие вопросы в своей базе данных:",
                    ui=TelegramUI(
                        buttons=[
                            Button(text=q, payload=q)
                            for q in ["Зачем мне использовать Arch?", "Почему мне не стоит использовать Arch?"]
                        ]
                    ),
                ),
            ),
            (
                TelegramMessage(callback_query="Зачем мне использовать Arch?"),
                TelegramMessage(text=faq["Зачем мне использовать Arch?"]),
            ),
            (
                TelegramMessage(callback_query="Почему мне не стоит использовать Arch?"),
                TelegramMessage(text=faq["Почему мне не стоит использовать Arch?"]),
            ),
            (
                TelegramMessage(text="Что такое Arch Linux?"),
                TelegramMessage(
                    text="Я нашел похожие вопросы в своей базе данных:",
                    ui=TelegramUI(buttons=[Button(text=q, payload=q) for q in ["Что такое Arch Linux?"]]),
                ),
            ),
            (TelegramMessage(callback_query="Что такое Arch Linux?"), TelegramMessage(text=faq["Что такое Arch Linux?"])),
            (
                TelegramMessage(text="Где я?"),
                TelegramMessage(
                    text="У меня нет ответа на этот вопрос. Вот список вопросов, на которые я могу дать ответ:",
                    ui=TelegramUI(buttons=[Button(text=q, payload=q) for q in faq]),
                ),
            ),
            (
                TelegramMessage(callback_query="Какие архитектуры поддерживает Arch?"),
                TelegramMessage(text=faq["Какие архитектуры поддерживает Arch?"]),
            ),
        )
    ],
)
async def test_happy_path(happy_path):
    check_happy_path(pipeline=pipeline, happy_path=happy_path)
