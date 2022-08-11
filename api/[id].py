from fastapi import FastAPI
import json


app = FastAPI()


@app.route('/')
async def index(request):
    return json({'hello': request})