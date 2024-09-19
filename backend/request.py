from flask import request, jsonify, make_response
from globals import FRONTEND_URL, CORS_ALLOW
from logger import Logger

class ApiException(Exception):
    def __init__(self, message, code=400):
        super().__init__(message)
        self.code = code

def handle_request(handler):
    try:
        result = handler()
        response = jsonify(result)
        if FRONTEND_URL is not None:
            response.headers.add('Access-Control-Allow-Origin', CORS_ALLOW)
        return response
    except ApiException as e:
        Logger().error(f"API error with code {e.code}: {e}")
        return make_response({"error": str(e)}, e.code)

def handle_request_with_data(handler):
    def inner():
        if request.headers.get("Content-Type") != "application/json":
            raise ApiException("Content-Type not supported!", 400)
        return handler(request.json)
    return handle_request(inner)
