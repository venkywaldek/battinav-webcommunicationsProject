from fastapi import FastAPI, Request


app = FastAPI()

@app.get("/")
def read_root():
    return { "msg": "Hello Venkat ,local docker!", "v": "0.1" }


@app.get("/hello")
def hello():
    return {"msh": "Hello venkat"}

@app.get("/api/ip")
def ip(request: Request):
    return{"ip" : request.client.host}