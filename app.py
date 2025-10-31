from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.chatbot_routes import chatbot_bp
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests (for React frontend)

# ✅ Register chatbot routes
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Cyber Crime Victim Assistance Chatbot API is running"}), 200

if __name__ == "__main__":
    mongo_uri = os.getenv("MONGO_URI")

    # ✅ Check if MONGO_URI is set before running
    if not mongo_uri:
        raise ValueError("❌ MONGO_URI environment variable is not set. Please add it in your .env file.")

    print("✅ MongoDB URI loaded successfully.")
    app.run(debug=True)
