import os

from dff.messengers.telegram import PollingTelegramInterface, TelegramMessenger
from dff.pipeline import Pipeline
from dff.script.core.context import Context

from .script import script
from .model import find_similar_questions


def question_processor(ctx: Context):
    last_request = ctx.last_request
    if last_request is None:
        return
    else:
        if last_request.annotations is None:
            last_request.annotations = {}
        else:
            if last_request.annotations.get("similar_questions") is not None:
                return
        if last_request.text is None:
            last_request.annotations["similar_questions"] = None
        else:
            last_request.annotations["similar_questions"] = find_similar_questions(last_request.text)

    ctx.set_last_request(last_request)


messenger = TelegramMessenger(os.getenv("TG_BOT_TOKEN", ""))
interface = PollingTelegramInterface(messenger=messenger)


pipeline = Pipeline.from_script(
    script=script,
    start_label=("proxy_flow", "start_node"),
    fallback_label=("proxy_flow", "fallback_node"),
    messenger_interface=interface,
    pre_services=[question_processor],
)
