from dff.pipeline import Pipeline
from dff.messengers.telegram import PollingTelegramInterface
from .main import script
from .utils import get_token

interface = PollingTelegramInterface(token=get_token())

pipeline = Pipeline.from_script(
    script = script,
    start_label=("general_flow", "start_node"),
    fallback_label=("general_flow", "fallback_node"),
    messenger_interface=interface,
)