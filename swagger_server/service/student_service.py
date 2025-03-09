import os
from bson.objectid import ObjectId
from pymongo import MongoClient

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@mongo:27017/student_db")
client = MongoClient(MONGO_URI)
db = client.get_database()
students_collection = db["students"]

def add(student):
    """Add a new student to the database."""
    if not student:
        return "Invalid student data", 400

    # Check if student already exists
    query = {"first_name": student.first_name, "last_name": student.last_name}
    existing_student = students_collection.find_one(query)
    if existing_student:
        return "already exists", 409

    # Insert new student
    result = students_collection.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)  # Convert ObjectId to string
    return student.student_id

def get_by_id(student_id):
    """Retrieve a student by ID."""
    if not ObjectId.is_valid(student_id):
        return "invalid id", 400

    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return "not found", 404

    student["student_id"] = str(student["_id"])  # Convert ObjectId to string
    student.pop("_id", None)  # Remove raw ObjectId
    return student

def delete(student_id):
    """Delete a student by ID."""
    if not ObjectId.is_valid(student_id):
        return "invalid id", 400

    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        return "not found", 404

    return student_id
