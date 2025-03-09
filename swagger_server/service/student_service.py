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
        # Insert the student into MongoDB
        result = students_collection.insert_one(student.to_dict())
        student.student_id = str(result.inserted_id)

        # Return a JSON response with the new student details
        return {
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name
        }, 200
    except Exception as e:
        print(f"Error adding student: {e}")
        return "internal server error", 500

def get_by_id(student_id):
    """Retrieve a student by ID."""
    try:
        # Find the student in MongoDB
        data = students_collection.find_one({"_id": ObjectId(student_id)})
        if not data:
            return "not found", 404

        # Return a JSON response including the first_name/last_name fields
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
        # Remove the student from MongoDB
        result = students_collection.delete_one({"_id": ObjectId(student_id)})
        if result.deleted_count == 0:
            return "not found", 404

        return student_id, 200
    except Exception as e:
        print(f"Error deleting student: {e}")
        return "internal server error", 500