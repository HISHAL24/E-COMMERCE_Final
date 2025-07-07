from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session
from flask_cors import CORS
from dto.catalogue_dto import catalogue
from service.catalogue_service import catalogueService
from service.authentication_service import AuthenticationService
import os

from flasgger import Swagger

from config.logger_config import logger



app = Flask(__name__, static_folder="frontend", static_url_path="")
logger.info("🚀 Starting the Flask application...")
app.secret_key = "supersecretkey"  # Required for session
# ✅ Enable CORS with support for cookies/session
CORS(app, supports_credentials=True)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Catalogue Management API",
        "description": "API for managing catalogues with login authentication.",
        "version": "1.0.0"
    }
})
# Initialize services
service = catalogueService()
auth_service = AuthenticationService()

# ✅ Serve index page only if logged in
@app.route("/")
def serve_index():
    if 'username' not in session:
        logger.warning("🔐 Unauthorized access attempt to index page.")
        return redirect("/login.html")
    logger.info("🏠Serving index page for user: %s", session["username"])
    return send_from_directory(app.static_folder, "index.html")

# ✅ Serve login page and other static files
@app.route("/<path:filename>")
def serve_static(filename):
    logger.info(f"📄Serving static file: {filename}")
    return send_from_directory(app.static_folder, filename)

# ✅ Handle login POST request
@app.route("/login", methods=["POST"])
def login():
    """
    Login User
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: admin123
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    logger.info(f"Login attempt for user: {username}")
    if auth_service.validate_user(username, password):
        session["username"] = username
        logger.info(f"User {username} logged in successfully.")
        return jsonify({"message": "Login successful"})
    logger.warning(f"Invalid login attempt for user: {username}")
    return jsonify({"error": "Invalid credentials"}), 401

# ✅ Logout clears session
@app.route("/logout", methods=["POST"])
def logout():
    """
    Logout User
    ---
    tags:
      - Authentication
    responses:
      200:
        description: Logout successful
    """
    user=session.pop("username", None)
    logger.info(f"User {user} logged out successfully.")
    return jsonify({"message": "Logged out"})

# -------------------------
# ✅ CRUD Operations (protected)
# -------------------------

@app.route("/catalogues", methods=["GET"])
def get_all_catalogues():
    """
    Get All Catalogues
    ---
    tags:
      - Catalogue
    responses:
      200:
        description: List of all catalogues
      401:
        description: Unauthorized
    """
    if 'username' in session:
        logger.warning("Unauthorized access attempt to get all catalogues.")
        return jsonify({"error": "Unauthorized"}), 401
    logger.info("Fetching all catalogues.")
    return jsonify(service.get_all_catalogues())

@app.route("/catalogues/<int:catalogue_id>", methods=["GET"])
def get_catalogue_by_id(catalogue_id):
    """
    Get Catalogue by ID
    ---
    tags:
      - Catalogue
    parameters:
      - name: catalogue_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Catalogue data
      401:
        description: Unauthorized
      404:
        description: Not found
    """
    if 'username' in session:
        logger.warning(f"Unauthorized access attempt to get catalogue with ID: {catalogue_id}")
        return jsonify({"error": "Unauthorized"}), 401
    logger.info(f"Fetching catalogue with ID: {catalogue_id}")
    result = service.get_catalogue_by_id(catalogue_id)
    if result:
        return jsonify(result)
    logger.error(f"Catalogue with ID {catalogue_id} not found.")
    return jsonify({"error": "Catalogue not found"}), 404

@app.route("/catalogues", methods=["POST"])
def create_catalogue():
    """
    Create a Catalogue
    ---
    tags:
      - Catalogue
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            catalogue_name:
              type: string
            catalogue_description:
              type: string
            effective_from:
              type: string
              format: date
              example: 2025-07-01
            effective_to:
              type: string
              format: date
              example: 2025-07-31
            status:
              type: string
              enum: [Active, Inactive]
    responses:
      201:
        description: Catalogue created
      401:
        description: Unauthorized
    """
    if 'username'  in session:
        logger.warning("Unauthorized access attempt to create catalogue.")
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    logger.info("Creating a new catalogue with data: %s", data)
    c = catalogue(**data)
    service.create_catalogue(c)
    return jsonify({"message": "Catalogue created"}), 201

@app.route("/catalogues/<int:catalogue_id>", methods=["PUT"])
def update_catalogue(catalogue_id):
    """
    Update a Catalogue
    ---
    tags:
      - Catalogue
    parameters:
      - name: catalogue_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          properties:
            catalogue_name:
              type: string
            catalogue_description:
              type: string
            effective_from:
              type: string
              format: date
            effective_to:
              type: string
              format: date
            status:
              type: string
    responses:
      200:
        description: Catalogue updated
      401:
        description: Unauthorized
    """
    if 'username' in session:
        logger.warning(f"Unauthorized access attempt to update catalogue with ID: {catalogue_id}")
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    logger.info(f"Updating catalogue with ID: {catalogue_id} with data: {data}")
    c = catalogue(**data)
    service.update_catalogue_by_id(catalogue_id, c)
    return jsonify({"message": "Catalogue updated"})

@app.route("/catalogues/<int:catalogue_id>", methods=["DELETE"])
def delete_catalogue(catalogue_id):
    """
    Delete a Catalogue
    ---
    tags:
      - Catalogue
    parameters:
      - name: catalogue_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Catalogue deleted
      401:
        description: Unauthorized
      404:
        description: Catalogue not found
    """
    if 'username' in session:
        logger.warning(f"Unauthorized access attempt to delete catalogue with ID: {catalogue_id}")
        return jsonify({"error": "Unauthorized"}), 401
    logger.info(f"Deleting catalogue with ID: {catalogue_id}")
    if service.delete_catalogue_by_id(catalogue_id):
        return jsonify({"message": "Catalogue deleted"})
    logger.error(f"Catalogue with ID {catalogue_id} not found for deletion.")
    return jsonify({"error": "Catalogue not found"}), 404

if __name__ == '__main__':
    logger.info("Starting the Flask server...")
    app.run(debug=True, host='127.0.0.1', port=5000)







