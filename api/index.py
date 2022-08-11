# from http.server import BaseHTTPRequestHandler


# class handler(BaseHTTPRequestHandler):

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type','text/plain')
#         self.end_headers()
#         self.wfile.write("Im Returning from you".encode())
#         return

from fastapi import FastAPI , Request
import json


app = FastAPI()


@app.get('/')
async def index(request: Request):
    return json({'hello': request})

@app.get('/{test}')
async def index(request: Request , test: str):
    return json({'hello': request , 
                 'test': test})