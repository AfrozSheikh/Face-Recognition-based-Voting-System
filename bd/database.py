from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/voting_system"
client = MongoClient(MONGO_URI)
db = client.get_database()

# Collections
users_collection = db["users"]
elections_collection = db["elections"]
votes_collection = db["votes"]
