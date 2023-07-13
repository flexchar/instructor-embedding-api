from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage
from InstructorEmbedding import INSTRUCTOR
import asyncio
import os

MODEL_NAME = os.environ.get("MODEL_NAME")

app = Sanic(__name__)
model = INSTRUCTOR(MODEL_NAME)


class EncodingEndpoint(HTTPMethodView):
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


app.add_route(EncodingEndpoint.as_view(), '/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
