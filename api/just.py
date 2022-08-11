from fastapi import FastAPI , Request

app = FastAPI()


@app.get('/')
async def index(request: Request):
    return {'hello': request}

@app.get('/{test}')
async def index(request: Request , test: str):
    return {'hello': request , 'test': test}