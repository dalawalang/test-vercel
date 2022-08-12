from fastapi import FastAPI , Request

app = FastAPI()


@app.get('/')
async def index(request: Request):
    return {'nospace': 'nothing to see here'}


@app.get('/{data}')
async def some_data(data: str):
    return {'data': data ,'status': 200}