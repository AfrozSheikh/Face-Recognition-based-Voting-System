# from flask import Blueprint, request, jsonify
# from app.database import users_collection, elections_collection, votes_collection
# from bson import ObjectId
# from app.utils.face_verification import verify_face

# voter_bp = Blueprint("voter", __name__)

# @voter_bp.route("/view_elections", methods=["POST"])
# def view_elections():
#     """Voter can see elections in their district"""
#     data = request.json
#     email = data.get("email")

#     user = users_collection.find_one({"email": email})
#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     elections = list(elections_collection.find({"district": user["district"], "status": "ongoing"}))
#     for election in elections:
#         election["_id"] = str(election["_id"])  # Convert ObjectId to string

#     return jsonify({"elections": elections}), 200

# @voter_bp.route("/vote", methods=["POST"])
# def vote():
#     """Voter casts a vote with face verification"""
#     data = request.json
#     email = data.get("email")
#     election_id = data.get("election_id")
#     candidate_name = data.get("candidate_name")
#     live_image_path = data.get("live_image_path")  # Path to the live image

#     user = users_collection.find_one({"email": email})
#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     if votes_collection.find_one({"voter_id": user["_id"], "election_id": ObjectId(election_id)}):
#         return jsonify({"message": "You have already voted"}), 403

#     # Face Verification
#     if not verify_face(user["face_embedding"], live_image_path):
#         return jsonify({"message": "Face verification failed"}), 403

#     # Update votes
#     elections_collection.update_one(
#         {"_id": ObjectId(election_id), "candidates.name": candidate_name},
#         {"$inc": {"candidates.$.votes": 1}}
#     )

#     votes_collection.insert_one({"voter_id": user["_id"], "election_id": ObjectId(election_id), "candidate": candidate_name})
    
#     return jsonify({"message": "Vote cast successfully"}), 200

# @voter_bp.route("/view_results", methods=["POST"])
# def view_results():
#     """Voter can view election results"""
#     data = request.json
#     email = data.get("email")

#     user = users_collection.find_one({"email": email})
#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     elections = list(elections_collection.find({"district": user["district"], "status": "completed"}))
#     for election in elections:
#         election["_id"] = str(election["_id"])  # Convert ObjectId to string

#     return jsonify({"results": elections}), 200

from flask import Blueprint, request, jsonify
from database import users_collection, elections_collection, votes_collection
from bson import ObjectId
from utils.face_verification import verify_face
  # Import JWT auth middleware

voter_bp = Blueprint("voter", __name__)

@voter_bp.route("/view_elections", methods=["GET"])

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

@voter_bp.route("/vote", methods=["POST"])

def vote():
    """Voter casts a vote with face verification"""
    data = request.json
    voter_id = request.user_id  # Extract voter ID from JWT
    election_id = data.get("election_id")
    candidate_name = data.get("candidate_name")
    live_image_path = data.get("live_image_path")  # Path to the live image

    user = users_collection.find_one({"_id": ObjectId(voter_id)})
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Check if voter already voted
    if votes_collection.find_one({"voter_id": ObjectId(voter_id), "election_id": ObjectId(election_id)}):
        return jsonify({"message": "You have already voted"}), 403

    # Face Verification
    if not verify_face(user["face_embedding"], live_image_path):
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

def view_results():
    """Voter can view election results"""
    voter_id = request.user_id  # Extract voter ID from JWT

    user = users_collection.find_one({"_id": ObjectId(voter_id)})
    if not user:
        return jsonify({"message": "User not found"}), 404

    elections = list(elections_collection.find({"district": user["district"], "status": "completed"}))
    
    for election in elections:
        election["_id"] = str(election["_id"])  # Convert ObjectId to string

    return jsonify({"results": elections}), 200
