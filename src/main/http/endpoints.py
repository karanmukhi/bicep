from fastapi import FastAPI, BackgroundTasks, UploadFile, File
import uvicorn
import os

from .endpointsLogic import *
from ..model.model import *
from ..model.table import *
from ..model.responseModel import *

app = FastAPI()

baseEndpoint: str = "/api/v1"
usersEndpoint: str = baseEndpoint + "/users"
workoutsEndpoint: str = baseEndpoint + "/workouts"
exerciseSetsEndpoint: str = baseEndpoint + "/exercise_sets"
accelDataEndpoint: str = baseEndpoint + "/acceleration_data"
gyroDataEndpoint: str = baseEndpoint + "/gyroscope_data"

@app.get(baseEndpoint)
def ping():
    return {"Ping": "Pong"}


@app.post(usersEndpoint, response_model=User)
def addUser(user: User) -> User:
    addRowsToTableLogic(UsersTable(), [user.dict()])
    return user


@app.post(workoutsEndpoint, response_model=Workout)
def addWorkout(workout: Workout) -> Workout:
    addRowsToTableLogic(WorkoutsTable(), [workout.dict()])
    return workout


@app.post(exerciseSetsEndpoint, response_model=ExerciseSet)
def addExerciseSet(exerciseSet: ExerciseSet) -> ExerciseSet:
    print([exerciseSet.dict()])
    addRowsToTableLogic(ExerciseSetsTable(), [exerciseSet.dict()])
    return exerciseSet


@app.post(accelDataEndpoint, response_model=SensorSuccessResponse)
def addAccelData(background_tasks: BackgroundTasks, acceleration_data: UploadFile = File(...)):
    numRows = addSensorDataByChunks(AccelDataTable(), acceleration_data)
    print("File length: " + str(numRows))
    return {"numRows": numRows}


@app.post(gyroDataEndpoint, response_model=SensorSuccessResponse)
def addGyroData(background_tasks: BackgroundTasks, gyroscope_data: UploadFile = File(...)):
    numRows = addSensorDataByChunks(GyroDataTable, gyroscope_data)
    print("File length: " + str(numRows))
    return {"numRows": numRows}


def serve():
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 8000)))
