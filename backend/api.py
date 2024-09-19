from gptscholar import GptScholar
from flask import Blueprint
from request import handle_request, handle_request_with_data, ApiException

gptscholar = GptScholar()

api = Blueprint("api", __name__)

@api.route("/ping")
def ping():
    return handle_request(lambda: { "response": "Pong!" })

@api.route("/prompt", methods=["POST"])
def run_prompt():
    def inner(data):
        if "prompt" not in data:
            raise ApiException("Missing 'prompt' field!", 400)
        return { "response": gptscholar.run(
            data["prompt"],
            data.get("initial_template_id", "1"),
            data.get("sparql_template_id", "1"),
            data.get("final_template_id", "1"),
        ) }

    return handle_request_with_data(inner)
