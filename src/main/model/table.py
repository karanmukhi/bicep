from google.cloud import bigquery
from typing import List


class BqTable:
    tableId: str
    schema: List[bigquery.SchemaField]


class UsersTable(BqTable):
    tableId = "users"
    schema = [
        bigquery.SchemaField("userID", "STRING"),
        bigquery.SchemaField("email", "STRING"),
        bigquery.SchemaField("name", "STRING"),
    ]


class WorkoutsTable(BqTable):
    tableId = "workouts"
    schema = [
        bigquery.SchemaField("workoutID", "STRING"),
        bigquery.SchemaField("userID", "STRING"),
        bigquery.SchemaField("time", "TIMESTAMP"),
    ]


class ExerciseSetsTable(BqTable):
    tableId = "exerciseSets"
    schema = [
        bigquery.SchemaField("exerciseSetID", "STRING"),
        bigquery.SchemaField("workoutID", "STRING"),
        bigquery.SchemaField("userID", "STRING"),
        bigquery.SchemaField("exercise", "STRING"),
        bigquery.SchemaField("reps", "INTEGER")
    ]

class SensorDataTable(BqTable):
    tableId = "notSpecified"
    schema = [
        bigquery.SchemaField("ms", "INTEGER"),
        bigquery.SchemaField("x", "FLOAT"),
        bigquery.SchemaField("y", "FLOAT"),
        bigquery.SchemaField("z", "FLOAT"),
        bigquery.SchemaField("reps", "INTEGER"),
        bigquery.SchemaField("exerciseSetID", "STRING"),
        bigquery.SchemaField("workoutID", "STRING"),
        bigquery.SchemaField("userID", "STRING"),
    ]

class AccelDataTable(SensorDataTable):
    tableId = "accelerationData"

class GyroDataTable(SensorDataTable):
    tableId = "gyroscopeData"