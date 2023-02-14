from dff.pipeline import Pipeline
from .main import script

pipeline = Pipeline.from_script(
    script = script,
    start_label=("general_flow", "start_node"),
    fallback_label=("general_flow", "fallback_node")
)