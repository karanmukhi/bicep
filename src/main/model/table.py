from typing import List


class BqTable:
    tableId: str


class UsersTable(BqTable):
    tableId = "users"


class WorkoutsTable(BqTable):
    tableId = "workouts"


class ExerciseSetsTable(BqTable):
    tableId = "exerciseSets"


class SensorDataTable(BqTable):
    tableId = "notSpecified"


class AccelDataTable(SensorDataTable):
    tableId = "accelerationData"


class GyroDataTable(SensorDataTable):
    tableId = "gyroscopeData"