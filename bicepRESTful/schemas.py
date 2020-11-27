from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# TODO separate into different files


class AccelerationDataBase(BaseModel):
    index: int
    accX: float
    accY: float
    accZ: float


class AccelerationData(AccelerationDataBase):
    exercise_set_id: int


class GyroscopeDataBase(BaseModel):
    index: int
    gyrX: float
    gyrY: float
    gyrZ: float


class GyroscopeData(GyroscopeDataBase):
    exercise_set_id: int


class ExerciseSetBase(BaseModel):
    workout_id: int
    exercise: str
    reps: int


class ExerciseSetCreate(ExerciseSetBase):
    pass


class ExerciseSet(ExerciseSetBase):
    id: int
    acceleration_data: List[AccelerationData]
    gyroscope_data: List[GyroscopeData]

    class Config:
        orm_mode = True


class WorkoutBase(BaseModel):
    user_id: int
    time: datetime


class WorkoutCreate(WorkoutBase):
    pass


class Workout(WorkoutBase):
    id: int
    exercise_sets: List[ExerciseSet]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    workouts: List[Workout] = []

    class Config:
        orm_mode = True
