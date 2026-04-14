#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    pushups = Exercise(
        name="Push Ups",
        category="strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="strength",
        equipment_needed=False
    )

    plank = Exercise(
        name="Plank",
        category="core",
        equipment_needed=False
    )

    treadmill = Exercise(
        name="Treadmill Run",
        category="cardio",
        equipment_needed=True
    )

    workout1 = Workout(
        date=date(2026, 4, 10),
        duration_minutes=45,
        notes="Upper body and core focus"
    )

    workout2 = Workout(
        date=date(2026, 4, 12),
        duration_minutes=30,
        notes="Conditioning session"
    )

    db.session.add_all([pushups, squats, plank, treadmill, workout1, workout2])
    db.session.commit()

    workout_exercise_1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=pushups.id,
        reps=15,
        sets=4
    )

    workout_exercise_2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=plank.id,
        sets=3,
        duration_seconds=60
    )

    workout_exercise_3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=treadmill.id,
        duration_seconds=1200
    )

    workout_exercise_4 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=squats.id,
        reps=20,
        sets=4
    )

    db.session.add_all([
        workout_exercise_1,
        workout_exercise_2,
        workout_exercise_3,
        workout_exercise_4
    ])
    db.session.commit()

    print("Database seeded successfully.")