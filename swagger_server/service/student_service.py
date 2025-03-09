import os
from bson.objectid import ObjectId
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/student_db")
client = MongoClient(MONGO_URI)
db = client.get_database()
students_collection = db["students"]

def add(student):
    """Add a new student to the database."""
    try:
        # ...existing code...
        # If the add is successful, explicitly return 200:
        return student.student_id, 200
    except Exception as e:
        print(f"Error adding student: {e}")
        return "internal server error", 500

def get_by_id(student_id):
    """Retrieve a student by ID."""
    try:
        # ...existing code...
        return student
    except Exception as e:
        print(f"Error getting student by ID: {e}")
        return "internal server error", 500

def delete(student_id):
    """Delete a student by ID."""
    try:
        # ...existing code...
        return student_id
    except Exception as e:
        print(f"Error deleting student: {e}")
        return "internal server error", 500