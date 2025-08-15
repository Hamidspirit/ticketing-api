from flask import jsonify

class ApiError(Exception):
    status_code = 400
    error = "Bad Request"

    def __init__(self, message="Bad Request", status_code=None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code
        self.message = message

    def to_response(self):
        response = jsonify({"error": self.message})
        response.status_code = self.status_code
        return response
    
class InvalidInputError(ApiError):
    status_code = 400

class UnauthorizedError(ApiError):
    status_code = 401

class NotFoundError(ApiError):
    status_code = 404

class ConflictError(ApiError):
    status_code = 409

# this error codes only get executed in prod.
# when debug mode is on they will not be executed
def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(err: ApiError):
        return err.to_response()

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"error": "Not Found"}), 404
    
    @app.errorhandler(405)
    def handle_405(err):
        return jsonify({"error": "Method Not Allowed"}), 405
    
    @app.errorhandler(500)
    def handle_500(err):
        return jsonify({"error": "Internal Server Error"}), 500
