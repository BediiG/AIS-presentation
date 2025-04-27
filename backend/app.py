from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)
from datetime import timedelta, datetime
import re

# ========================
# 🔁 Toggle Mode Here
USE_COOKIES = True
# ========================

# Initialize app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
app.config["SECRET_KEY"] = "your_secret_key"
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"

# Token expiration settings
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=36000)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(seconds=360000)

# Token delivery mode
if USE_COOKIES:
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Enable in production
    app.config["JWT_COOKIE_SECURE"] = True        # True in production with HTTPS
else:
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Enable CORS (adjust for production)
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": "https://localhost:5173"}},
    methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"]
)

# Password strength checker
def is_password_strong(password):
    errors = []
    if len(password) < 8:
        errors.append("at least 8 characters")
    if not re.search(r'[A-Z]', password):
        errors.append("one uppercase letter")
    if not re.search(r'[a-z]', password):
        errors.append("one lowercase letter")
    if not re.search(r'\d', password):
        errors.append("one digit")
    if not re.search(r'\W', password):
        errors.append("one special character")
    return errors

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    failed_attempts = db.Column(db.Integer, default=0)
    last_failed_time = db.Column(db.DateTime, default=None)

# Initialize the database
with app.app_context():
    db.create_all()

# Register route
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    password_errors = is_password_strong(password)
    if password_errors:
        return jsonify({
            "message": "Password is too weak.",
            "requirements": password_errors
        }), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# Login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    LOCKOUT_THRESHOLD = 5
    LOCKOUT_TIME = timedelta(minutes=10)

    if user:
        if user.failed_attempts >= LOCKOUT_THRESHOLD:
            if datetime.utcnow() - user.last_failed_time < LOCKOUT_TIME:
                return jsonify({"message": "Account temporarily locked. Try again later."}), 403
            else:
                user.failed_attempts = 0
                db.session.commit()

        if bcrypt.check_password_hash(user.password, password):
            user.failed_attempts = 0
            db.session.commit()
            additional_claims = {"username": user.username}
            access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

            if USE_COOKIES:
                response = jsonify({"message": "Login successful (cookie mode)"})
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response
            else:
                return jsonify({
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                })
        else:
            user.failed_attempts += 1
            user.last_failed_time = datetime.utcnow()
            db.session.commit()
            return jsonify({"message": "Invalid username or password"}), 401

    return jsonify({"message": "Invalid username or password"}), 401

# Refresh token route
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    claims = get_jwt()
    additional_claims = {"username": claims["username"]}
    new_access_token = create_access_token(identity=str(current_user), additional_claims=additional_claims)

    if USE_COOKIES:
        response = jsonify({"message": "Token refreshed (cookie mode)"})
        set_access_cookies(response, new_access_token)
        return response
    else:
        return jsonify(access_token=new_access_token)

# Protected route
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    claims = get_jwt()
    username = claims["username"]
    return jsonify({"message": f"Hello {username}, welcome to the protected page (via {'cookies' if USE_COOKIES else 'header'})"})

# Logout route
@app.route("/logout", methods=["POST"])
def logout():
    if USE_COOKIES:
        response = jsonify({"message": "Logged out (cookies cleared)"})
        unset_jwt_cookies(response)
        return response
    else:
        return jsonify({"message": "Logout: no cookies to clear"})

if __name__ == "__main__":
    app.run(ssl_context=("backend-cert.pem", "backend-key.pem"), port=5000)
