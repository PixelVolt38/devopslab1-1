import connexion
from swagger_server.models.student import Student  # noqa: E501
from swagger_server.service.student_service import add, delete, get_by_id

def add_student(body=None):  # noqa: E501
    """Add a new student

    Adds an item to the system # noqa: E501
    
    :param body: Student item to add
    :type body: dict | bytes
    
    :rtype: dict | tuple
    """
    if not connexion.request.is_json:
        return {"error": "Invalid JSON input"}, 400

    body = Student.from_dict(connexion.request.get_json())  # noqa: E501
    student_id = add(body)

    if isinstance(student_id, tuple):  # Check if it's an error response
        return {"error": student_id[0]}, student_id[1]

    return {"student_id": student_id}, 201

def delete_student(student_id):  # noqa: E501
    """Deletes a student

    Deletes a single student  # noqa: E501

    :param student_id: The student ID
    :type student_id: str

    :rtype: dict | tuple
    """
    result = delete(student_id)

    if isinstance(result, tuple):  # Error handling
        return {"error": result[0]}, result[1]

    return {"message": f"Student {student_id} deleted"}, 200

def get_student_by_id(student_id):  # noqa: E501
    """Gets a student by ID

    Returns a single student # noqa: E501

    :param student_id: The student ID
    :type student_id: str

    :rtype: dict | tuple
    """
    student = get_by_id(student_id)

    if isinstance(student, tuple):  # Error handling
        return {"error": student[0]}, student[1]

    return student, 200
