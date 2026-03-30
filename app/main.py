from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return { "msg": "Hello Venkat ,local docker!", "v": "0.1" }


@app.get("/hello")
def hello():
    return {"msh": "Hello venkat"}

@app.get("/api/ip")
def ip(request: Request):
    return{"ip" : request.client.host}