from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)

    workouts = relationship("Workout", back_populates="user")


class Workout(Base):
    __tablename__ = "workout"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    time = Column(DateTime)

    user = relationship("User", back_populates="workouts")
    exercise_sets = relationship("ExerciseSet", back_populates="workout")


class ExerciseSet(Base):
    __tablename__ = "exercise_set"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workout.id"))
    exercise = Column(String, index=True)
    reps = Column(Integer)

    workout = relationship("Workout", back_populates="exercise_sets")
    acceleration_data = relationship("AccelerationData", back_populates="exercise_set")
    gyroscope_data = relationship("GyroscopeData", back_populates="exercise_set")


class AccelerationData(Base):
    __tablename__ = "acceleration_data"

    index = Column(Integer, primary_key=True, index=True)
    exercise_set_id = Column(Integer, ForeignKey("exercise_set.id"), primary_key=True)
    accX = Column(Float)
    accY = Column(Float)
    accZ = Column(Float)

    exercise_set = relationship("ExerciseSet", back_populates="acceleration_data")


class GyroscopeData(Base):
    __tablename__ = "gyroscope_data"

    index = Column(Integer, primary_key=True, index=True)
    exercise_set_id = Column(Integer, ForeignKey("exercise_set.id"), primary_key=True)
    accX = Column(Float)
    accY = Column(Float)
    accZ = Column(Float)

    exercise_set = relationship("ExerciseSet", back_populates="gyroscope_data")