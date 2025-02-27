from bson import ObjectId
from database import elections_collection

class Election:
    @staticmethod
    def create_election(title, district, start_time, end_time):
        """Create a new election"""
        if start_time >= end_time:
            return {"error": "Start time must be before end time"}
        election_data = {
            "title": title,
            "district": district,
            "candidates": [],
            "start_time": start_time,
            "end_time": end_time,
            "status": "ongoing"
        }
        return elections_collection.insert_one(election_data).inserted_id
    @staticmethod
    def get_all_elections():
        """Fetch all elections"""
        return list(elections_collection.find({}, {"_id": 1, "title": 1, "district": 1, "status": 1}))


    @staticmethod
    def add_candidate(election_id, candidate_name, party):
        """Add a candidate to an election"""
        if not elections_collection.find_one({"_id": ObjectId(election_id)}):
            return {"error": "Election not found"}
        return elections_collection.update_one(
            {"_id": ObjectId(election_id)},
            {"$push": {"candidates": {"name": candidate_name, "party": party, "votes": 0}}}
        )

    @staticmethod
    def get_election_by_id(election_id):
        """Fetch election by ID"""
        return elections_collection.find_one({"_id": ObjectId(election_id)})

    @staticmethod
    def update_vote_count(election_id, candidate_name):
        """Increase the vote count for a candidate"""
        election = elections_collection.find_one({"_id": ObjectId(election_id)})
    
        if not election:
            return {"error": "Election not found"}

        if election["status"] == "completed":
            return {"error": "Voting is closed for this election"}
        return elections_collection.update_one(
            {"_id": ObjectId(election_id), "candidates.name": candidate_name},
            {"$inc": {"candidates.$.votes": 1}}
        )

    @staticmethod
    def declare_results(election_id):
        """Mark election as completed and get winner"""
        election = elections_collection.find_one({"_id": ObjectId(election_id)})
    
        if not election:
            return {"error": "Election not found"}

        if election["status"] == "completed":
             return {"error": "Results already declared"}

        candidates = election["candidates"]
        if not candidates:
                return {"error": "No candidates in this election"}

        winner = max(candidates, key=lambda c: c["votes"])  # Candidate with max votes

        elections_collection.update_one(
         {"_id": ObjectId(election_id)},
        {"$set": {"status": "completed", "winner": winner}} )

        return {"message": "Election completed", "winner": winner}

    
