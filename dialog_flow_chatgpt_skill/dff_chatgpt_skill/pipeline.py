"""
Pipeline
---------
This module defines the bot pipeline including additional handlers
"""
import logging

from dff.pipeline import Pipeline
from dff.messengers.telegram import PollingTelegramInterface
from .main import script
from .utils import get_token

interface = PollingTelegramInterface(token=get_token())


def debug_service(ctx):
    logging.debug(ctx.dict())


pipeline = Pipeline.from_script(
    script=script,
    pre_services=[debug_service],
    post_services=[debug_service],
    start_label=("general_flow", "start_node"),
    fallback_label=("general_flow", "fallback_node"),
    messenger_interface=interface,
)
