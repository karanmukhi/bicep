from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    userID = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)


class Workout(Base):
    __tablename__ = "workout"

    workoutID = Column(String, primary_key=True, index=True)
    userID = Column(String)
    time = Column(DateTime)

class ExerciseSet(Base):
    __tablename__ = "exercise_set"

    exerciseSetID = Column(String, primary_key=True, index=True)
    workoutID = Column(String)
    userID = Column(String)
    exercise = Column(String, index=True)
    reps = Column(Integer)


class AccelerationData(Base):
    __tablename__ = "acceleration_data"

    index = Column(Integer, index=True)
    accX = Column(Float)
    accY = Column(Float)
    accZ = Column(Float)
    exerciseSetID = Column(String)
    workoutID = Column(String)
    userID = Column(String)

class GyroscopeData(Base):
    __tablename__ = "gyroscope_data"

    index = Column(Integer, index=True)
    accX = Column(Float)
    accY = Column(Float)
    accZ = Column(Float)
    exerciseSetID = Column(String)
    workoutID = Column(String)
    userID = Column(String)