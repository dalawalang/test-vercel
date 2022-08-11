from fastapi import FastAPI , Request

app = FastAPI()


@app.get('/')
async def index(request: Request):
    print('request ', dir(request))
    print('request ', request.url)
    return {'this is the message boi': 'cannot do anything lol'}
