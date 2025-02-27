from bson import ObjectId
from database import elections_collection

class Election:
    @staticmethod
    def create_election(title, district, start_time, end_time):
        """Create a new election"""
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
    def add_candidate(election_id, candidate_name, party):
        """Add a candidate to an election"""
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
        return elections_collection.update_one(
            {"_id": ObjectId(election_id), "candidates.name": candidate_name},
            {"$inc": {"candidates.$.votes": 1}}
        )

    @staticmethod
    def declare_results(election_id):
        """Mark election as completed"""
        return elections_collection.update_one(
            {"_id": ObjectId(election_id)},
            {"$set": {"status": "completed"}}
        )
