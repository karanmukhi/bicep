from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_workout(db: Session, workout_id: int):
    return db.query(models.Workout).filter(models.Workout.id == workout_id).first()


def create_workout(db: Session, workout: schemas.WorkoutCreate):
    db_workout = models.Workout(**workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def get_set_by_id(db: Session, set_id: int):
    return db.query(models.ExerciseSet).filter(models.ExerciseSet.id == set_id).first()


def create_set(db: Session, exerciseSet: schemas.ExerciseSetCreate):
    db_set = models.ExerciseSet(**exerciseSet.dict())
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set


def insert_acceleration_data(
    db: Session, acceleration_data
):  # TODO type of acceleration_data Dataframe?
    # TODO insert after responding?
    acceleration_data_dict = acceleration_data.to_dict("records")
    db.bulk_insert_mappings(models.AccelerationData, acceleration_data_dict)
    db.commit()
    print(
        "Set: {} Rows: {} acc data".format(
            acceleration_data["exercise_set_id"][0], len(acceleration_data_dict)
        )
    )


def insert_gyroscope_data(db: Session, gyroscope_data):
    gyroscope_data_dict = gyroscope_data.to_dict("records")
    db.bulk_insert_mappings(models.GyroscopeData, gyroscope_data_dict)
    db.commit()
    print(
        "Set: {} Rows: {} gyr data".format(
            gyroscope_data["exercise_set_id"][0], len(gyroscope_data_dict)
        )
    )
    return len(gyroscope_data_dict)
