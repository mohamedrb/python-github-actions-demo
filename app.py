import os
import certifi
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

mongo = PyMongo()  # initialize WITHOUT app

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/test_student_db")
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

    mongo.init_app(app, tlsCAFile=certifi.where())

    # Home
    @app.route('/')
    def index():
        students = mongo.db.students.find()
        return render_template('index.html', students=students)

    # Add
    @app.route('/add', methods=['GET', 'POST'])
    def add_student():
        if request.method == 'POST':
            mongo.db.students.insert_one({
                "name": request.form['name'],
                "email": request.form['email'],
                "course": request.form['course']
            })
            return redirect(url_for('index'))
        return render_template('add_student.html')

    # Update
    @app.route('/update/<student_id>', methods=['GET', 'POST'])
    def update_student(student_id):
        student = mongo.db.students.find_one({"_id": ObjectId(student_id)})

        if request.method == 'POST':
            mongo.db.students.update_one(
                {"_id": ObjectId(student_id)},
                {"$set": {
                    "name": request.form['name'],
                    "email": request.form['email'],
                    "course": request.form['course']
                }}
            )
            return redirect(url_for('index'))

        return render_template('update_student.html', student=student)

    # Delete
    @app.route('/delete/<student_id>')
    def delete_student(student_id):
        mongo.db.students.delete_one({"_id": ObjectId(student_id)})
        return redirect(url_for('index'))

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
