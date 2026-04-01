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

#tillfälligt data

temp_rooms = [ 
         {"room_number" : 101, "price" : 1  , "room_type" : "double room"}, 
         {"room_number" : 202, "price" : 2  , "room_type" : "single room"}, 
         {"room_number" : 303, "price" : 3  , "room_type" : "Suite"}
    ]
 
@app.get("/")
def read_root():
    return("Välkommen till hötell  API")

@app.get("/rooms")
def rooms():
    return  temp_rooms

@app.put("/rooms")
def rooms():
    return  temp_rooms

@app.post("/bookings")
def create_booking():
    return{"msg" : "booking skapad"}

