import os
from functools import reduce
from pymongo import MongoClient

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client['students_db']
students_collection = db['students']

def add(student=None):
    queries = []
    queries.append({'first_name': student.first_name})
    queries.append({'last_name': student.last_name})
    query = {'$and': queries}
    res = students_collection.find_one(query)
    if res:
        return 'already exists', 409

    result = students_collection.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)
    return student.student_id

def get_by_id(student_id=None, subject=None):
    student = students_collection.find_one({'_id': student_id})
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    print(student)
    return student

def delete(student_id=None):
    result = students_collection.delete_one({'_id': student_id})
    if result.deleted_count == 0:
        return 'not found', 404
    return student_id
