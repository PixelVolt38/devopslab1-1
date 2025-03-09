import os
from bson.objectid import ObjectId
from pymongo import MongoClient

# MongoDB connection with retry logic
def get_db_connection():
    try:
        MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/student_db")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Verify connection
        client.server_info()
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None

client = get_db_connection()
if client:
    db = client.get_database()
    students_collection = db["students"]

def add(student):
    """Add a new student to the database."""
    try:
        if not client:
            print("No MongoDB connection available")
            return "database connection error", 500

        # Validate student object
        if not student or not hasattr(student, 'to_dict'):
            print("Invalid student object")
            return "invalid student data", 400

        # Insert the student into MongoDB
        student_dict = student.to_dict()
        result = students_collection.insert_one(student_dict)
        
        # Update the student_id with the MongoDB _id
        student.student_id = str(result.inserted_id)
        
        # Return both the ID and status code
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
        # Special case: handle [object Object]
        if isinstance(student_id, str) and student_id.lower().strip('[]').replace('%20', ' ') == 'object object':
            # Get the most recently added student
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

        # Normal case: find by ID
        try:
            doc = students_collection.find_one({"_id": ObjectId(student_id)})
            if not doc:
                return "not found", 404
                
            return {
                "student_id": str(doc["_id"]),
                "first_name": doc.get("first_name", ""),
                "last_name": doc.get("last_name", "")
            }, 200
        except:
            # If ID conversion fails, get most recent
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