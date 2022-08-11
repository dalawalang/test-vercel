from fastapi import FastAPI , Request

app = FastAPI()


@app.get('/')
async def index(request: Request):
    print('request ', request)
    return {'just visiting': str(request.url)}
