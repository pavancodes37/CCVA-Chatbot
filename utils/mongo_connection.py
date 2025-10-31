from pymongo import MongoClient
import os

def get_db_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ccva_chatbot"]
    return db

def save_incident(crime_type):
    db = get_db_connection()
    incidents = db["incidents"]
    incidents.insert_one({"crime_type": crime_type})
