from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.route('/student', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        new_student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
            amount_due=data['amount_due']
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Student created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'dob': student.dob.strftime('%Y-%m-%d'),
        'amount_due': student.amount_due
    })

@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.get_json()
        student = Student.query.get_or_404(id)
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
        student.amount_due = data['amount_due']
        db.session.commit()
        return jsonify({'message': 'Student updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'dob': student.dob.strftime('%Y-%m-%d'),
        'amount_due': student.amount_due
    } for student in students])

if __name__ == '__main__':
    app.run(debug=True)
