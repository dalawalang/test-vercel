from fastapi import FastAPI , Request

app = FastAPI()

@app.get('/api/{function}')
async def some_data(function: str):
    return {'function': function ,'status': 200}


@app.get('/api/test/{file}')
async def some_data(file: str):
    return {'file': file ,'status': 401}