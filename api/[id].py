from fastapi import FastAPI , Request
import json


app = FastAPI()


@app.get('/')
async def index(request: Request):
    return json({'hello': request})

@app.get('/{test}')
async def index(request: Request , test: str):
    return json({'hello': request , 
                 'test': test})