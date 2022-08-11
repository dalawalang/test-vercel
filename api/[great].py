from fastapi import FastAPI , Request

app = FastAPI()


@app.get('/')
async def index(request: Request):
    print('request ', dir(request))
    return {'this is the message boi': str(request['path'])}
