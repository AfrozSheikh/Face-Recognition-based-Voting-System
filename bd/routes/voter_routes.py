
from flask import Blueprint, request, jsonify
from database import users_collection, elections_collection, votes_collection
from bson import ObjectId
from utils.face_verification import verify_face
 
import jwt
from functools import wraps
from flask import request, jsonify
from config import SECRET_KEY
from bson import ObjectId
from database import users_collection

def voter_required(f):
    """Voter authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token missing"}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data["role"] != "voter":
                return jsonify({"message": "Unauthorized"}), 403

            user = users_collection.find_one({"_id": ObjectId(data["user_id"])})
            if not user:
                return jsonify({"message": "User not found"}), 404

            if not user.get("is_approved", False):
                return jsonify({"message": "Voter not approved by admin"}), 403

            request.user_id = data["user_id"]  # Attach voter ID to request
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 403

        return f(*args, **kwargs)
    
    return decorated_function

voter_bp = Blueprint("voter", __name__)

@voter_bp.route("/view_elections", methods=["GET"])
@voter_required
def view_elections():
    """Voter can see elections in their district"""
    voter_id = request.user_id  # Extract voter ID from JWT

    user = users_collection.find_one({"_id": ObjectId(voter_id)})
    if not user:
        return jsonify({"message": "User not found"}), 404

    elections = list(elections_collection.find({"district": user["district"], "status": "ongoing"}))
    
    for election in elections:
        election["_id"] = str(election["_id"])  # Convert ObjectId to string

    return jsonify({"elections": elections}), 200

# @voter_bp.route("/vote", methods=["POST"])
# @voter_required
# def vote():
#     """Voter casts a vote with face verification"""
#     data = request.json
#     voter_id = request.user_id  # Extract voter ID from JWT
#     election_id = data.get("election_id")
#     candidate_name = data.get("candidate_name")
#     live_image_path = data.get("live_image_path")  # Path to the live image

#     user = users_collection.find_one({"_id": ObjectId(voter_id)})
#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     # Check if voter already voted
#     if votes_collection.find_one({"voter_id": ObjectId(voter_id), "election_id": ObjectId(election_id)}):
#         return jsonify({"message": "You have already voted"}), 403

#     # Face Verification
#     if not verify_face(user["face_embedding"], live_image_path):
#         return jsonify({"message": "Face verification failed"}), 403

#     # Update votes
#     result = elections_collection.update_one(
#         {"_id": ObjectId(election_id), "candidates.name": candidate_name},
#         {"$inc": {"candidates.$.votes": 1}}
#     )

#     if result.modified_count == 0:
#         return jsonify({"message": "Candidate not found"}), 404

#     votes_collection.insert_one({
#         "voter_id": ObjectId(voter_id),
#         "election_id": ObjectId(election_id),
#         "candidate": candidate_name
#     })
    
#     return jsonify({"message": "Vote cast successfully"}), 200

# @voter_bp.route("/vote", methods=["POST"])
# @voter_required
# def vote():
#     """Voter casts a vote with face verification"""
#     data = request.json
#     voter_id = request.user_id
#     election_id = data.get("election_id")
#     candidate_name = data.get("candidate_name")
#     live_image_path = data.get("live_image_path")  # Path to the live image

#     user = users_collection.find_one({"_id": ObjectId(voter_id)})
#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     # Check if voter already voted
#     if votes_collection.find_one({"voter_id": ObjectId(voter_id), "election_id": ObjectId(election_id)}):
#         return jsonify({"message": "You have already voted"}), 403

#     # Fetch election and check if it's ongoing
#     election = elections_collection.find_one({"_id": ObjectId(election_id)})
#     if not election:
#         return jsonify({"message": "Election not found"}), 404

#     if election["status"] != "ongoing":
#         return jsonify({"message": "Voting is closed"}), 403

#     # Face Verification
#     if not verify_face(user["face_embedding"], live_image_path):
#         return jsonify({"message": "Face verification failed"}), 403

#     # Update votes
#     result = elections_collection.update_one(
#         {"_id": ObjectId(election_id), "candidates.name": candidate_name},
#         {"$inc": {"candidates.$.votes": 1}}
#     )

#     if result.modified_count == 0:
#         return jsonify({"message": "Candidate not found"}), 404

#     votes_collection.insert_one({
#         "voter_id": ObjectId(voter_id),
#         "election_id": ObjectId(election_id),
#         "candidate": candidate_name
#     })
    
#     return jsonify({"message": "Vote cast successfully"}), 200


import base64
import cv2
import numpy as np

@voter_bp.route("/vote", methods=["POST"])
@voter_required
def vote():
    """Voter casts a vote with face verification"""
    data = request.json
    voter_id = request.user_id
    election_id = data.get("election_id")
    candidate_name = data.get("candidate_name")
    live_image_base64 = data.get("live_image")  # Base64 image from frontend

    user = users_collection.find_one({"_id": ObjectId(voter_id)})
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Decode base64 image
    live_image_data = base64.b64decode(live_image_base64.split(",")[1])
    nparr = np.frombuffer(live_image_data, np.uint8)
    live_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Check if voter already voted
    if votes_collection.find_one({"voter_id": ObjectId(voter_id), "election_id": ObjectId(election_id)}):
        return jsonify({"message": "You have already voted"}), 403

    # Fetch election and check if it's ongoing
    election = elections_collection.find_one({"_id": ObjectId(election_id)})
    if not election:
        return jsonify({"message": "Election not found"}), 404

    if election["status"] != "ongoing":
        return jsonify({"message": "Voting is closed"}), 403

    # Face Verification
    if not verify_face(user["face_embedding"], live_image):
        return jsonify({"message": "Face verification failed"}), 403

    # Update votes
    result = elections_collection.update_one(
        {"_id": ObjectId(election_id), "candidates.name": candidate_name},
        {"$inc": {"candidates.$.votes": 1}}
    )

    if result.modified_count == 0:
        return jsonify({"message": "Candidate not found"}), 404

    votes_collection.insert_one({
        "voter_id": ObjectId(voter_id),
        "election_id": ObjectId(election_id),
        "candidate": candidate_name
    })
    
    return jsonify({"message": "Vote cast successfully"}), 200
@voter_bp.route("/view_results", methods=["GET"])
@voter_required
def view_results():
    """Voter can view election results"""
    voter_id = request.user_id  # Extract voter ID from JWT

    user = users_collection.find_one({"_id": ObjectId(voter_id)})
    if not user:
        return jsonify({"message": "User not found"}), 404

    elections = list(elections_collection.find(
        {"district": user["district"], "status": "completed"},
        {"_id": 1, "name": 1, "candidates": 1, "winner": 1}
    ))

    for election in elections:
        election["_id"] = str(election["_id"])  # Convert ObjectId to string
        for candidate in election["candidates"]:
            candidate["votes"] = candidate.get("votes", 0)  # Ensure votes are included

    return jsonify({"results": elections}), 200  

# @voter_bp.route("/view_results", methods=["GET"])
# @voter_required
# def view_results():
#     """Voter can view election results"""
#     voter_id = request.user_id  # Extract voter ID from JWT

#     user = users_collection.find_one({"_id": ObjectId(voter_id)})
#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     elections = list(elections_collection.find({"district": user["district"], "status": "completed"}))
    
#     for election in elections:
#         election["_id"] = str(election["_id"])  # Convert ObjectId to string

#     return jsonify({"results": elections}), 200
