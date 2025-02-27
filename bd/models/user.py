from database import users_collection
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name, email, password, district, face_embedding=None, role="voter", is_approved=False):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.district = district
        self.role = role
        self.face_embedding = face_embedding
        self.is_approved = is_approved

    def save(self):
        """Save user to MongoDB"""
        if users_collection.find_one({"email": self.email}):
           return {"error": "Email already exists"}
        user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "district": self.district,
            "role": self.role,
            "face_embedding": self.face_embedding,
            "is_approved": self.is_approved
        }
        users_collection.insert_one(user_data)

    @staticmethod
    def find_by_email(email):
        """Find a user by email"""
        return users_collection.find_one({"email": email})

    @staticmethod
    def verify_password(stored_password, password):
        """Verify hashed password"""
        return check_password_hash(stored_password, password)
