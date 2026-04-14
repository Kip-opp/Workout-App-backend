# Flask SQLAlchemy Workout App

## Project Description
This is a Flask backend API for a workout tracking application. The API allows users to create workouts, create exercises, and link exercises to workouts through a join table that stores activity details such as reps, sets, and duration.

## Features
- Create, view, and delete workouts
- Create, view, and delete exercises
- Add an exercise to a workout
- Store workout activity details such as reps, sets, and duration
- Validate data at schema, model, and table levels
- Manage schema changes with Flask-Migrate

## Technologies Used
- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pipenv

## Project Structure

```txt
flask-SqlAlchemy-workout-app/
├── README.md
├── Pipfile
├── Pipfile.lock
├── migrations/
├── instance/
└── server/
    ├── app.py
    ├── models.py
    ├── schemas.py
    └── seed.py
```

## Installation

1. Clone the repository:
```bash
git clone git@github.com:Kip-opp/Workout-App-backend.git
cd flask-SqlAlchemy-workout-app
```

2. Install dependencies:
```bash
pipenv install
```

3. Activate the virtual environment:
```bash
pipenv shell
```

## Database Setup

Set the Flask app:
```bash
export FLASK_APP=server/app.py
```

Apply migrations:
```bash
flask db upgrade
```

Seed the database:
```bash
python server/seed.py
```

## Run the Server

```bash
python server/app.py
```

The API runs on:

```txt
http://127.0.0.1:5555
```

## API Endpoints

### Workouts
- `GET /workouts`
- `GET /workouts/<id>`
- `POST /workouts`
- `DELETE /workouts/<id>`

### Exercises
- `GET /exercises`
- `GET /exercises/<id>`
- `POST /exercises`
- `DELETE /exercises/<id>`

### WorkoutExercises
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`

## Example Request Bodies

### Create Workout
```json
{
  "date": "2026-04-14",
  "duration_minutes": 45,
  "notes": "Upper body workout"
}
```

### Create Exercise
```json
{
  "name": "Push Ups",
  "category": "strength",
  "equipment_needed": false
}
```

### Add Exercise to Workout
```json
{
  "reps": 15,
  "sets": 4
}
```

## Curl Examples

### 1. Get all workouts
```bash
curl http://127.0.0.1:5555/workouts
```

### 2. Get all exercises
```bash
curl http://127.0.0.1:5555/exercises
```

### 3. Create a new workout
```bash
curl -X POST http://127.0.0.1:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-04-14",
    "duration_minutes": 45,
    "notes": "Upper body session"
  }'
```

### 4. Add an exercise to a workout
```bash
curl -X POST http://127.0.0.1:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{
    "reps": 15,
    "sets": 4
  }'
```

## Validation Rules

### Workout
- `duration_minutes` must be greater than 0
- `date` cannot be in the future

### Exercise
- `name` must be unique
- `name` must be at least 2 characters long
- `category` must be one of:
  - `strength`
  - `cardio`
  - `mobility`
  - `core`
  - `conditioning`

### WorkoutExercise
- `workout_id` and `exercise_id` must be valid
- At least one of `reps`, `sets`, or `duration_seconds` should be provided
- Numeric values must be greater than 0
- The same exercise cannot be added twice to the same workout

## Testing
You can test the API with curl, Postman, or Insomnia. For JSON POST requests, include the `Content-Type: application/json` header so Flask parses the request body correctly.[web:141][web:145]

## Author
Built as a Flask + SQLAlchemy + Marshmallow backend project.