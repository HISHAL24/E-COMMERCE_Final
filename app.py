from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session
from flask_cors import CORS
from dto.catalogue_dto import catalogue
from service.catalogue_service import catalogueService
from service.authentication_service import AuthenticationService
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
app.secret_key = "supersecretkey"  # Required for session

# ✅ Enable CORS with support for cookies/session
CORS(app, supports_credentials=True)

service = catalogueService()
auth_service = AuthenticationService()

# ✅ Serve index page only if logged in
@app.route("/")
def serve_index():
    if 'username' not in session:
        return redirect("/login.html")
    return send_from_directory(app.static_folder, "index.html")

# ✅ Serve login page and other static files
@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# ✅ Handle login POST request
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if auth_service.validate_user(username, password):
        session["username"] = username
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

# ✅ Logout clears session
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"message": "Logged out"})

# -------------------------
# ✅ CRUD Operations (protected)
# -------------------------

@app.route("/catalogues", methods=["GET"])
def get_all_catalogues():
    if 'username' in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(service.get_all_catalogues())

@app.route("/catalogues/<int:catalogue_id>", methods=["GET"])
def get_catalogue_by_id(catalogue_id):
    if 'username' in session:
        return jsonify({"error": "Unauthorized"}), 401
    result = service.get_catalogue_by_id(catalogue_id)
    if result:
        return jsonify(result)
    return jsonify({"error": "Catalogue not found"}), 404

@app.route("/catalogues", methods=["POST"])
def create_catalogue():
    if 'username'  in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    c = catalogue(**data)
    service.create_catalogue(c)
    return jsonify({"message": "Catalogue created"}), 201

@app.route("/catalogues/<int:catalogue_id>", methods=["PUT"])
def update_catalogue(catalogue_id):
    if 'username' in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    c = catalogue(**data)
    service.update_catalogue_by_id(catalogue_id, c)
    return jsonify({"message": "Catalogue updated"})

@app.route("/catalogues/<int:catalogue_id>", methods=["DELETE"])
def delete_catalogue(catalogue_id):
    if 'username' in session:
        return jsonify({"error": "Unauthorized"}), 401
    service.delete_catalogue_by_id(catalogue_id)
    return jsonify({"message": "Catalogue deleted"})

if __name__ == '__main__':
    app.run(debug=True)
