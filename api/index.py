# from http.server import BaseHTTPRequestHandler


# class handler(BaseHTTPRequestHandler):

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type','text/plain')
#         self.end_headers()
#         self.wfile.write("Im Returning from you".encode())
#         return

from fastapi import FastAPI , Request

app = FastAPI()


@app.get('/')
async def index(request: Request):
    return {'hello': request}

@app.get('/{test}')
async def index(request: Request , test: str):
    return {'hello': request , 'test': test}