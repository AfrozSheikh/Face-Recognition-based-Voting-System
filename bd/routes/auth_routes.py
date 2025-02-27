from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime
from config import SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD_HASH
from models.user import User

auth_bp = Blueprint("auth", __name__)

def generate_token(user_id, role):
    """Generate JWT token"""
    payload = {
        "user_id": str(user_id),
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    """Voter Signup Route"""
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    district = data.get("district")

    if User.find_by_email(email):
        return jsonify({"message": "User already exists"}), 400

    new_user = User(name, email, password, district)
    new_user.save()

    return jsonify({"message": "Signup successful. Wait for admin approval."}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """Voter & Admin Login Route"""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Admin Login
    if email == ADMIN_EMAIL :
        token = generate_token("admin", "admin")
        return jsonify({"message": "Admin login successful", "token": token}), 200

    # Voter Login
    user = User.find_by_email(email)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user["is_approved"]:
        return jsonify({"message": "Admin approval pending"}), 403

    if not User.verify_password(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_token(user["_id"], "voter")
    return jsonify({"message": "Login successful", "token": token}), 200
