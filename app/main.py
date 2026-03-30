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

# @app.get("/")
# def read_root():
#     return { "msg": "Hello Venkat ,local docker!", "v": "0.1" }


@app.get("/hello")
def hello():
    return {"msg": "Hello venkat"}



rooms = [ {"number" : 1, "persons" : 1  , "name" : "singleroom"}, {"number" : 2, "persons" : 2  , "name" : "doubleroom"},  {"number" : 3, "persons" : 3  , "name" : "Suiteroom"}]
 
@app.get("/items/rooms")
def read_root():
    return rooms

@app.get("/hotel")

def hotel():
    return {"msg": "Hello Hotel"}



@app.get("/api/ip")
def ip(request: Request):
    return{"ip" : request.client.host}