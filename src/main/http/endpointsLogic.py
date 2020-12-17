import psycopg2
from typing import Dict
from fastapi import HTTPException, status, UploadFile
import simplejson as json
import pandas as pd

from ..config.config import getConfig
from ..model.table import *

def getDbConnection():
    config = getConfig()
    conn = psycopg2.connect(
        database=config['database'], user=config['user'], password=config['password'], host=config['host'],
        port=config['port']
    )
    return conn


def addRowsToTableLogic(table: BqTable, rows: List[Dict[str, any]]):
    conn = getDbConnection()
    cursor = conn.cursor()
    for rowDict in rows:
        query = f"INSERT INTO {table.tableId} VALUES {', '.join(list(map(str, rowDict.values())))};"
        cursor.execute(query)
    try:
        conn.commit()
        print("New rows have been added.")
    except Exception as err:
        print(f"Encountered errors while inserting rows: {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )


def addSensorDataByChunks(table: BqTable(), data: UploadFile) -> int:
    numRows: int = 0
    for chunkDf in pd.read_csv(
            data.file,
            chunksize=10 ** 4,
            header=None,
            names=["x", "y", "z", "exerciseSetID", "workoutID", "userID"]):
        chunkDf["ms"] = chunkDf.index * 20  # 20 ms between each reading
        numRows += len(chunkDf.index)
        rows = json.loads(chunkDf.to_json(orient="records"))
        addRowsToTableLogic(table, rows)
        return numRows