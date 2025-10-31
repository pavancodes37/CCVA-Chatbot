from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.chatbot_routes import chatbot_bp
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# ✅ Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests (for React frontend)

# ✅ Register chatbot routes
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")

# ✅ MongoDB Connection
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("❌ MONGO_URI environment variable is not set. Please add it in your .env file.")

try:
    client = MongoClient(mongo_uri)
    db = client["ccva_chatbot"]
    print("✅ MongoDB connected successfully.")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Cyber Crime Victim Assistance Chatbot API is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
