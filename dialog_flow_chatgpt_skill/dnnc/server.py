import logging
import time
import os
from argparse import Namespace

import torch
import sentry_sdk
from flask import Flask, request, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration

from models.utils import load_intent_datasets, sample
from models.dnnc import DNNC
from intent_predictor import DnncIntentPredictor

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), integrations=[FlaskIntegration()])

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_CONFIDENCE = 0.9
ZERO_CONFIDENCE = 0.0
MAX_SEQ_LENGTH = 128
TRAIN_FILE_PATH = os.getenv("TRAIN_FILE_PATH")
DEV_FILE_PATH = os.getenv("DEV_FILE_PATH")
MODEL_PATH = "roberta_nli"

try:
    train_examples, dev_examples = load_intent_datasets(TRAIN_FILE_PATH, DEV_FILE_PATH, True)
    sampled_tasks = [sample(5, train_examples)]
    if torch.cuda.is_available():
        no_cuda = False
    else:
        no_cuda = True
    dnnc = DNNC(MODEL_PATH, Namespace(**{"no_cuda": no_cuda, "bert_model": "roberta-base", "max_seq_length": MAX_SEQ_LENGTH}))
    intent_predictor = DnncIntentPredictor(dnnc, sampled_tasks[0])
    logger.info("predictor is ready")
except Exception as e:
    sentry_sdk.capture_exception(e)
    logger.exception(e)
    raise e

app = Flask(__name__)
logging.getLogger("werkzeug").setLevel("WARNING")


@app.route("/respond", methods=["POST"])
def respond():
    st_time = time.time()
    contexts = request.json.get("dialog_contexts", [])

    try:
        responses = []
        confidences = []
        for context in contexts:
            response, score, _ = intent_predictor.predict_intent(context[-1])
            if len(response) > 3:
                # drop too short responses
                responses += [response]
                confidences += [score]
    except Exception as exc:
        logger.exception(exc)
        sentry_sdk.capture_exception(exc)
        responses = [""] * len(contexts)
        confidences = [ZERO_CONFIDENCE] * len(contexts)

    total_time = time.time() - st_time
    logger.info(f"Keywords storyGPT exec time: {total_time:.3f}s")
    return jsonify(list(zip(responses, confidences)))