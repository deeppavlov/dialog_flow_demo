import json
from pathlib import Path

import numpy
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('clips/mfaq')

with open(Path(__file__).parent / "faq.json", "r", encoding="utf-8") as file:
    faq = json.load(file)


def find_similar_questions(question: str):
    questions = list(map(lambda x: "<Q>" + x, faq.keys()))
    q_emb, *faq_emb = model.encode(["<Q>" + question] + questions)

    emb_with_scores = tuple(zip(questions, map(lambda x: numpy.linalg.norm(x - q_emb), faq_emb)))

    filtered_embeddings = tuple(sorted(filter(lambda x: x[1] < 10, emb_with_scores), key=lambda x: x[1]))

    result = []
    for question, score in filtered_embeddings:
        question = question.removeprefix("<Q>")
        result.append(question)
    return result