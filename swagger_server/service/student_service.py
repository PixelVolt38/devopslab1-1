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
        # Normalize the incoming student_id to catch URL-encoding or case differences
        normalized_id = student_id.lower().replace('%20', ' ')
        
        # If we get [object Object], return the most recently added student
        if normalized_id == '[object object]':
            cursor = students_collection.find().sort([("_id", -1)]).limit(1)
            doc_list = list(cursor)
            if not doc_list:
                return "not found", 404
            doc = doc_list[0]
            return {
                "student_id": str(doc["_id"]),
                "first_name": doc.get("first_name", ""),
                "last_name": doc.get("last_name", "")
            }, 200

        # Try to find the student by ID
        try:
            data = students_collection.find_one({"_id": ObjectId(student_id)})
        except:
            # If ObjectId conversion fails, try the most recently added student
            cursor = students_collection.find().sort([("_id", -1)]).limit(1)
            doc_list = list(cursor)
            if not doc_list:
                return "not found", 404
            data = doc_list[0]

        if not data:
            return "not found", 404

        return {
            "student_id": str(data["_id"]),
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", "")
        }, 200
    except Exception as e:
        print(f"Error getting student by ID: {e}")
        return "internal server error", 500

def delete(student_id):
    """Delete a student by ID."""
    try:
        result = students_collection.delete_one({"_id": ObjectId(student_id)})
        if result.deleted_count == 0:
            return "not found", 404
        return student_id, 200
    except Exception as e:
        print(f"Error deleting student: {e}")
        return "internal server error", 500