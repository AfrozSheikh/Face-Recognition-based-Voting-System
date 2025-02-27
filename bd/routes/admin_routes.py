
from flask import Blueprint, request, jsonify
from database import users_collection, elections_collection
from bson import ObjectId
import datetime
import jwt
from functools import wraps
from werkzeug.security import check_password_hash
from config import SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD_HASH

admin_bp = Blueprint("admin", __name__)

def admin_required(f):
    """Admin authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token missing"}), 403

        try:
            # ✅ Remove "Bearer " prefix
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            print("Decoded Token:", token)  # Debugging

            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            if data["role"] != "admin":
                return jsonify({"message": "Unauthorized"}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token", "token": token}), 403

        return f(*args, **kwargs)

    return decorated_function


# def admin_required(f):
#     """Admin authentication decorator"""
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         token = request.headers.get("Authorization")
    
#         if not token:
#             return jsonify({"message": "Token missing"}), 403

#         try:
#             data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             if data["role"] != "admin":
#                 return jsonify({"message": "Unauthorized"}), 403
#         except jwt.ExpiredSignatureError:
#             return jsonify({"message": "Token expired"}), 403
#         except jwt.InvalidTokenError:
#             return jsonify({"message": "Invalid token","tokken":token}), 403

#         return f(*args, **kwargs)
    
#     return decorated_function

@admin_bp.route("/approve_voter", methods=["POST"])
@admin_required
def approve_voter():
    """Admin approves a voter"""
    data = request.json
    email = data.get("email")
    
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"message": "User not found"}), 404

    users_collection.update_one({"email": email}, {"$set": {"is_approved": True}})
    return jsonify({"message": "Voter approved successfully"}), 200

@admin_bp.route("/reject_voter", methods=["POST"])
@admin_required
def reject_voter():
    """Admin rejects a voter"""
    data = request.json
    email = data.get("email")

    users_collection.delete_one({"email": email})
    return jsonify({"message": "Voter rejected and removed"}), 200

@admin_bp.route("/create_election", methods=["POST"])
@admin_required
def create_election():
    """Admin creates a new election"""
    data = request.json
    print(data)
    title = data.get("title")
    district = data.get("district")
    start_time_str = data.get("start_time")  # Example: "2025-02-27T21:51"

# ✅ Convert frontend format to backend expected format
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")

    end_time_str = data.get("end_time")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M")
    
    election_data = {
        "title": title,
        "district": district,
        "candidates": [],
        "start_time": start_time,
        "end_time": end_time,
        "status": "ongoing"
    }
    elections_collection.insert_one(election_data)

    return jsonify({"message": "Election created successfully"}), 201



@admin_bp.route("/pending_voters", methods=["GET"])
@admin_required
def get_pending_voters():
    """Fetch all voters who are not yet approved"""
    pending_voters = users_collection.find({"is_approved": False}, {"_id": 1, "name": 1, "email": 1})
    
    voter_list = [{"_id": str(voter["_id"]), "name": voter["name"], "email": voter["email"]} for voter in pending_voters]
    
    return jsonify({"pendingVoters": voter_list}), 200

# @admin_bp.route("/approve_voter/<voter_id>", methods=["POST"])
# @admin_required
# def approve_voter(voter_id):
#     """Approve or reject a voter"""
#     data = request.json
#     status = data.get("status")

#     if status not in ["approved", "rejected"]:
#         return jsonify({"error": "Invalid status"}), 400

#     users_collection.update_one({"_id": ObjectId(voter_id)}, {"$set": {"status": status}})
#     return jsonify({"message": f"Voter {status}"}), 200

@admin_bp.route("/add_candidate", methods=["POST"])
@admin_required
def add_candidate():
    """Admin adds a candidate to an election"""
    data = request.json
    election_id = data.get("election_id")
    candidate_name = data.get("name")
    party = data.get("party")
    
    election = elections_collection.find_one({"_id": ObjectId(election_id)})
    if not election:
        return jsonify({"message": "Election not found"}), 404

    elections_collection.update_one(
        {"_id": ObjectId(election_id)},
        {"$push": {"candidates": {"name": candidate_name, "party": party, "votes": 0}}}
    )

    return jsonify({"message": "Candidate added successfully"}), 200

# @admin_bp.route("/declare_results", methods=["POST"])
# @admin_required
# def declare_results():
#     """Admin declares the election results"""
#     data = request.json
#     election_id = data.get("election_id")
    
#     election = elections_collection.find_one({"_id": ObjectId(election_id)})
#     if not election:
#         return jsonify({"message": "Election not found"}), 404

#     elections_collection.update_one(
#         {"_id": ObjectId(election_id)},
#         {"$set": {"status": "completed"}}
#     )

#     return jsonify({"message": "Election results declared"}), 200

from models.election_model import Election  # Import Election model

@admin_bp.route("/declare_results", methods=["POST"])
@admin_required
def declare_results():
    """Admin declares the election results"""
    data = request.json
    election_id = data.get("election_id")

    result = Election.declare_results(election_id)

    return jsonify(result), 200 if "message" in result else 400  # Return appropriate status code
