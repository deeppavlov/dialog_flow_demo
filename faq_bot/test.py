from os import getenv

import pytest
from dff.utils.testing.common import check_happy_path
from dff.messengers.telegram import TelegramMessage, TelegramUI, CallbackQuery
from dff.script import RESPONSE
from dff.script.core.message import Button

from bot.script import script
from bot.bot import pipeline
from bot.model import faq


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "scenario",
    [
        (
            (TelegramMessage(text="/start"), script["proxy_flow"]["welcome_node"][RESPONSE]),
            (
                TelegramMessage(text="Why use arch?"),
                TelegramMessage(
                    text="I found similar questions in my database:",
                    ui=TelegramUI(
                        buttons=[
                            Button(text=q, payload=q) for q in [
                                'Why would I want to use Arch?', 'Why would I not want to use Arch?'
                            ]
                        ]
                    )
                )
            ),
            (
                TelegramMessage(
                    commands=[CallbackQuery(data='Why would I want to use Arch?')]
                ),
                TelegramMessage(
                    text=faq['Why would I want to use Arch?']
                )
            ),
            (
                TelegramMessage(
                    commands=[CallbackQuery(data='Why would I not want to use Arch?')]
                ),
                TelegramMessage(
                    text=faq['Why would I not want to use Arch?']
                )
            ),
            (
                TelegramMessage(
                    text="What is arch linux?"
                ),
                TelegramMessage(
                    text="I found similar questions in my database:",
                    ui=TelegramUI(
                        buttons=[
                            Button(text=q, payload=q) for q in ['What is Arch Linux?']
                        ]
                    )
                )
            ),
            (
                TelegramMessage(
                    commands=[CallbackQuery(data='What is Arch Linux?')]
                ),
                TelegramMessage(
                    text=faq['What is Arch Linux?']
                )
            ),
            (
                TelegramMessage(
                    text="where am I?"
                ),
                TelegramMessage(
                    text="I don't have an answer to that question. Here's a list of questions I know an answer to:",
                    ui=TelegramUI(
                        buttons=[
                            Button(text=q, payload=q) for q in faq
                        ]
                    )
                )
            ),
            (
                TelegramMessage(
                    commands=[CallbackQuery(data='What architectures does Arch support?')]
                ),
                TelegramMessage(
                    text=faq['What architectures does Arch support?']
                )
            )
        )
    ]
)
async def test_scenario(scenario):
    check_happy_path(pipeline=pipeline, happy_path=scenario)
