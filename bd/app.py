# from flask import Flask
# from routes.auth_routes import auth_bp
# from routes.admin_routes import admin_bp
# from routes.voter_routes import voter_bp

# app = Flask(__name__)

# # Register Blueprints (routes)
# app.register_blueprint(auth_bp, url_prefix="/auth")
# app.register_blueprint(admin_bp, url_prefix="/admin")
# app.register_blueprint(voter_bp, url_prefix="/voter")

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask
# from flask_cors import CORS
# from routes.auth_routes import auth_bp
# from routes.admin_routes import admin_bp
# from routes.voter_routes import voter_bp

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}) # Enable CORS for all routes

# # Register Blueprints (routes)
# app.register_blueprint(auth_bp, url_prefix="/auth")
# app.register_blueprint(admin_bp, url_prefix="/admin")
# app.register_blueprint(voter_bp, url_prefix="/voter")

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.voter_routes import voter_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(voter_bp, url_prefix="/voter")

if __name__ == "__main__":
    app.run(debug=True)
