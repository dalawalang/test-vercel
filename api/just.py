from fastapi import FastAPI , Request

app = FastAPI()


@app.get('/')
async def index(request: Request):
    print('request ', request)
    return {'hello': str(request)}

@app.get('/{test}')
async def index(request: Request , test: str):
    print('request : ',request)
    return {'hello': str(request) , 'test': test}