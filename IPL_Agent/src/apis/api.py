import os
import pandas as pd
import fastapi
import aiofiles
from fastapi import File, UploadFile, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from controllers.controller import read_csv_file
from models.model import IPL_MatchInfoCSV, IPL_MatchDataCSV


router = APIRouter()


@router.post('/upload_matchdata')
async def upload_matchdata(
    file: UploadFile = File(...)
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
    except Exception as e:
        return HTTPException(status_code = 422, detail = str(e))

    return JSONResponse(status_code = 200, content = {"message": "IPL Match Data uploaded successfully"})


@router.post('/upload_matchinfo')
async def upload_matchinfo(
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
    except Exception as e:
        return HTTPException(status_code = 404, detail= str(e))
    return JSONResponse(status_code=200, content = "IPL Match Info Uploaded Successfully")