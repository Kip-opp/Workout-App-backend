from marshmallow import Schema, fields, validate, validates_schema, ValidationError

ALLOWED_CATEGORIES = ["strength", "cardio", "mobility", "core", "conditioning"]


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=80))
    category = fields.Str(required=True, validate=validate.OneOf(ALLOWED_CATEGORIES))
    equipment_needed = fields.Bool(required=True)
    workouts = fields.List(
        fields.Nested(lambda: WorkoutSchema(exclude=("exercises", "workout_exercises", "notes"))),
        dump_only=True
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(load_only=True)
    exercise_id = fields.Int(load_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    exercise = fields.Nested(
        ExerciseSchema(only=("id", "name", "category", "equipment_needed")),
        dump_only=True
    )

    @validates_schema
    def validate_workout_exercise_payload(self, data, **kwargs):
        if not any([
            data.get("reps"),
            data.get("sets"),
            data.get("duration_seconds")
        ]):
            raise ValidationError(
                "At least one of reps, sets, or duration_seconds must be provided."
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)

    exercises = fields.List(
        fields.Nested(ExerciseSchema(only=("id", "name", "category", "equipment_needed"))),
        dump_only=True
    )

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema),
        dump_only=True
    )


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()