import pytest
from app import create_app, mongo
from bson.objectid import ObjectId

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test_student_db"

    client = app.test_client()

    with app.app_context():
        mongo.db.students.delete_many({})
        mongo.db.students.insert_one({
            "_id": ObjectId("66fddff25f4b5f6a0a123456"),
            "name": "Test Student",
            "email": "test@student.com",
            "course": "Flask"
        })

    yield client

    with app.app_context():
        mongo.cx.drop_database("test_student_db")
