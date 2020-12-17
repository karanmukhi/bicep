from pydantic import BaseModel
import datetime


class User(BaseModel):
    userID: str
    email: str
    name: str


class Workout(BaseModel):
    workoutID: str
    userID: str
    time: datetime.datetime


class ExerciseSet(BaseModel):
    exerciseSetID: str
    workoutID: str
    userID: str
    exercise: str
    reps: int


class SensorData(BaseModel):
    ms: int
    x: float
    y: float
    z: float
    exerciseSetID: str
    workoutID: str
    userID: str
