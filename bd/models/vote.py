from bson import ObjectId
from database import votes_collection

class Vote:
    @staticmethod
    def record_vote(voter_id, election_id, candidate_name, timestamp):
        """Store a voter's vote"""
        vote_data = {
            "voter_id": ObjectId(voter_id),
            "election_id": ObjectId(election_id),
            "candidate": candidate_name,
            "timestamp": timestamp
        }
        return votes_collection.insert_one(vote_data)

    @staticmethod
    def has_voted(voter_id, election_id):
        """Check if a voter has already voted in an election"""
        return votes_collection.find_one({"voter_id": ObjectId(voter_id), "election_id": ObjectId(election_id)}) is not None
