from fastapi import FastAPI

app = FastAPI()

@app.get('/api/{process}')
async def some_data(process):
    cached_cashflow = [process * 2]
  
    return {'functionv12': cached_cashflow,'status': 200}


@app.delete('/api/{process}')
async def some_data(process):
    return {'delete': process,'status': 200}
