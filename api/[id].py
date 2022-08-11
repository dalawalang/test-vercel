from fastapi import FastAPI
import json


app = FastAPI()


@app.get('/')
async def index(request):
    return json({'hello': request})