from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import BackgroundTasks
from fastapi import File, UploadFile
import pandas as pd
from sqlalchemy.orm import Session

from . import crud, models, schemas

from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO tablenames and paths should be singular or plural --- /user or /users
@app.post("/user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return crud.create_user(db, user)


# @app.get("/user", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@app.post("/workout", response_model=schemas.Workout)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, workout.userID)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not registered for workout upload",
        )
    return crud.create_workout(db, workout)


@app.post("/exercise_set", response_model=schemas.ExerciseSet)
def create_set(exerciseSet: schemas.ExerciseSetCreate, db: Session = Depends(get_db)):
    db_workout = crud.get_workout(db, exerciseSet.workoutID)
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workout not registered for set upload",
        )
    created_set = crud.create_set(db, exerciseSet)
    return created_set


@app.post("/acceleration_data")
def insert_acceleration_data(
    background_tasks: BackgroundTasks,
    acceleration_data: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    acceleration_data_df = pd.read_csv(
        acceleration_data.file,
        header=None,
        names=["accX", "accY", "accZ", "exerciseSetID", "workoutID", "userID"],
    )
    acceleration_data_df["index"] = acceleration_data_df.index
    background_tasks.add_task(crud.insert_acceleration_data, db, acceleration_data_df)
    return {"Size": len(acceleration_data_df.index)}


@app.post("/gyroscope_data")
def insert_gyroscope_data(
    background_tasks: BackgroundTasks,
    gyroscope_data: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    gyroscope_data_df = pd.read_csv(
        gyroscope_data.file,
        header=None,
        names=["gyrX", "gyrY", "gyrZ", "exerciseSetID", "workoutID", "userID"],
    )
    gyroscope_data_df["index"] = gyroscope_data_df.index
    gyroscope_data_df["exercise_set_id"] = set_id
    background_tasks.add_task(crud.insert_gyroscope_data, db, gyroscope_data_df)
    return {"Size": len(gyroscope_data_df.index)}


if __name__ == "__main__":
    pass
    # models.Base.metadata.drop_all(bind=engine, checkfirst=True)

    # import uvicorn

    # uvicorn.run(app, host="0.0.0.0", port=5000)