from flask import Flask, request, jsonify
import os
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
    workout_exercise_schema,
)

app = Flask(__name__, instance_relative_config=True)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "instance", "app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(DB_PATH)}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

print("DATABASE URI:", app.config["SQLALCHEMY_DATABASE_URI"])
print("INSTANCE PATH:", app.instance_path)


@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"errors": err.messages}), 400


@app.get("/")
def home():
    return jsonify({"message": "Workout API is running"}), 200


@app.get("/workouts")
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.post("/workouts")
def create_workout():
    try:
        data = workout_schema.load(request.get_json())
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Database integrity error"]}), 400


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()
    return "", 204


@app.get("/exercises")
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.post("/exercises")
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Exercise name must be unique"]}), 400


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()
    return "", 204


@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    try:
        payload = request.get_json() or {}
        payload["workout_id"] = workout_id
        payload["exercise_id"] = exercise_id

        data = workout_exercise_schema.load(payload)
        workout_exercise = WorkoutExercise(**data)

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            {"errors": ["This exercise is already added to that workout"]}
        ), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)

print("DATABASE URI:", app.config["SQLALCHEMY_DATABASE_URI"])
print("INSTANCE PATH:", app.instance_path)