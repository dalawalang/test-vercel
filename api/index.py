from fastapi import FastAPI , Request

app = FastAPI()

@app.get('/api')
async def some_data():
    return {'functionv12': 'fool' ,'status': 200}


@app.delete('/api')
async def some_data():
    return {'delete': 'dlete' ,'status': 200}
