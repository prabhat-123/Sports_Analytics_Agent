import os
import pandas as pd
import aiofiles
from fastapi import File, UploadFile, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from controllers.controller import read_csv_file
from utils.enums import TableName
from models.model import IPL_MatchInfoCSV, IPL_MatchDataCSV
from db.models import IPL_MatchData, IPL_MatchInfo
from db.postgres import insert_into_postgres, delete_user_data

router = APIRouter()


@router.post('/upload_matchdata')
async def upload_matchdata(
    table_name: TableName,
    file: UploadFile = File(...),
    ):
    if not file.filename.endswith('.csv'):
        return HTTPException(status_code = 400, detail= "Updated file is not a CSV file")
    os.makedirs('uploadfiles/', exist_ok=True)
    path = f'uploadfiles/{file.filename}'
    async with aiofiles.open(path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    data = read_csv_file(path)
    try:
        clean_data = [IPL_MatchDataCSV(**row) for row in data]
        # Assuming `IPL_MatchData` is your SQLAlchemy ORM model
        clean_data_sql = [IPL_MatchData(**row.dict()) for row in clean_data]
        delete_user_data(table_name)
        insert_into_postgres(clean_data_sql)
    except Exception as e:
        return HTTPException(status_code = 422, detail = str(e))

    return JSONResponse(status_code = 200, content = {"message": "IPL Match Data uploaded successfully"})


@router.post('/upload_matchinfo')
async def upload_matchinfo(
    table_name: TableName,
    file: UploadFile = File(...)
):
    if not file.filename.endswith('.csv'):
        return HTTPException(status_code=400, detail="Uploaded file is not a CSV file")
    
    os.makedirs('uploadfiles/', exist_ok=True)
    path = f'uploadfiles/{file.filename}'
    async with aiofiles.open(path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    data = read_csv_file(path)
    try:
        clean_data = [IPL_MatchInfoCSV(**row) for row in data]
        # Assuming `IPL_MatchData` is your SQLAlchemy ORM model
        clean_data_sql = [IPL_MatchInfo(**row.dict()) for row in clean_data]
        delete_user_data(table_name)
        insert_into_postgres(clean_data_sql)
    except Exception as e:
        return HTTPException(status_code = 404, detail= str(e))
    return JSONResponse(status_code=200, content = "IPL Match Info Uploaded Successfully")