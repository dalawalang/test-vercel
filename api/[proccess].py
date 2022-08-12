from fastapi import FastAPI

app = FastAPI()

@app.get('/api/{process}')
async def some_data(process):
    return {'functionv12': process,'status': 200}


@app.delete('/api/{process}')
async def some_data(process):
    return {'delete': process,'status': 200}
