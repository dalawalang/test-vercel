from fastapi import FastAPI , Request

app = FastAPI()


@app.get('/')
async def index(request: Request):
    return {'nospace': 'nothing to see here'}
