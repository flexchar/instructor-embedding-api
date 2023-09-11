from sanic import Sanic, Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage
from InstructorEmbedding import INSTRUCTOR
import asyncio
import os

MODEL_NAME = os.environ.get("MODEL_NAME")

print(f"Loading model {MODEL_NAME}...")

app = Sanic(__name__)
model = INSTRUCTOR("/model")

@app.route("/", methods=["POST"])
async def post(self, request):
    instructions_sentences = request.json.get('input')

    if not instructions_sentences:
        raise InvalidUsage("Input is missing or invalid")

    embeddings = model.encode(instructions_sentences)

    return json({
        "model": MODEL_NAME,
        "data": embeddings.tolist()
    })

@app.route("/health", methods=["GET"])
async def health_check(request):
    return json({"status": "ok"})


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

@app.route("/classify", methods=["POST"])
async def classify(request: Request):
    to_detect_string = request.json.get('input')
    categories = request.json.get('categories')
    instruction = request.json.get('instruction')
    
    # Each category is a list of objects, an object has id and a few examples.
    # Encode each example and store in a list with the category id.
    # Then, encode the input string and compare with the list of examples.
    # Return the category with the highest similarity.
    # https://github.com/xlang-ai/instructor-embedding#use-customized-embeddings-for-information-retrieval
    
    if not to_detect_string:
        raise InvalidUsage("Input is missing or invalid")

    if not categories:
        raise InvalidUsage("Categories are missing or invalid")

    for category in categories:
        category["embeddings"] = model.encode([[instruction, example] for example in category["examples"]])

    to_detect_embedding = model.encode([[instruction, to_detect_string]])[0]
    
    highest_similarity = 0
    detected_category = None
    for category in categories:
        similarities = cosine_similarity([to_detect_embedding], category["embeddings"])
        avg_similarity = np.mean(similarities)
        category["similarity"] = avg_similarity
        # print(f"Category {category['id']} has similarity {avg_similarity}")
        if avg_similarity > highest_similarity:
            highest_similarity = avg_similarity
            detected_category = category

    # Sort categories by similarity and only return id and similarity
    analyzed_categories = [{"id": c["id"], "similarity": round(float(c["similarity"]), 3)} for c in categories]
    analyzed_categories = sorted(analyzed_categories, key=lambda c: c["similarity"], reverse=True)

    return json({
        "model": MODEL_NAME,
        "data": detected_category["id"],
        "categories": analyzed_categories
    })


@app.middleware("request")
async def ensure_json(request):
    # Ensure request is JSON
    if request.content_type != "application/json":
        raise InvalidUsage("Content type must be application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
