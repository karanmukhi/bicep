from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# TODO separate into different files


class AccelerationDataBase(BaseModel):
    index: int
    accX: float
    accY: float
    accZ: float
    exerciseSetID: str
    workoutID: str
    userID: str


class AccelerationData(AccelerationDataBase):
    pass


class GyroscopeDataBase(BaseModel):
    index: int
    gyrX: float
    gyrY: float
    gyrZ: float
    exerciseSetID: str
    workoutID: str
    userID: str


class GyroscopeData(GyroscopeDataBase):
    pass


class ExerciseSetBase(BaseModel):
    exerciseSetID: str
    workoutID: str
    userID: str,
    exercise: str
    reps: int


class ExerciseSetCreate(ExerciseSetBase):
    pass


class ExerciseSet(ExerciseSetBase):
    pass

class WorkoutBase(BaseModel):
    workoutID: str
    userID: str
    time: datetime


class WorkoutCreate(WorkoutBase):
    pass


class Workout(WorkoutBase):
    pass

class UserBase(BaseModel):
    userID: str
    email: str
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    pass
