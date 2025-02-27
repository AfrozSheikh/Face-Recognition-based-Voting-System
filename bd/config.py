import os

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
MONGO_URI = "mongodb://localhost:27017/voting_system"

# Admin credentials (hashed password)
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD_HASH = "$2b$12$KIX/Zc48jGtE8TmtD6g9peb.YzCU0R9FShrHXLhSKTC/U/uY/gMZy"  # Hash for 'admin123'
