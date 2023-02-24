import os

from dff.messengers.telegram import PollingTelegramInterface
from dff.pipeline import Pipeline

from dialog_graph import graph
from pipeline_services import pre_services


if __name__ == "__main__":
    tg_token = os.getenv("TG_BOT_TOKEN", "")

    if tg_token:
        pipeline = Pipeline.from_script(
            script=graph.script,
            start_label=("service_flow", "start_node"),
            fallback_label=("service_flow", "fallback_node"),
            messenger_interface=PollingTelegramInterface(token=os.getenv("TG_BOT_TOKEN", "")),
            pre_services=pre_services.services,  # pre-services run before bot sends a response
        )
        pipeline.run()
    else:
        raise RuntimeError(
            "Telegram token (`TG_BOT_TOKEN`) is not set. `TG_BOT_TOKEN` can be set by `.env` file"
            " to get more info look at README.md"
        )
