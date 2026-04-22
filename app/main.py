from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.security import APIKeyHeader
from datetime import date
from typing import Optional
from app.db import get_conn, create_schema


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date
    addinfo: Optional[str] = None

class BookingStars(BaseModel):
    stars:int

@app.on_event("startup")
def startup():
    create_schema()

api_key_header = APIKeyHeader( name = "X-API-Key", auto_error = False )

def validate_api_key(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail={"error": "API key missing"})

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM hotel_guests WHERE api_key = %s
        """, [api_key])
        guest = cur.fetchone()

    if not guest:
        raise HTTPException(status_code=401, detail={"error": "Guest missing"})

    return guest   

#main route for this api
@app.get("/")
def root():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT 'databasen funkar' as msg
        """)
        result = cur.fetchone()
    return {"msg": "Välkommen till hostells bokning API", "db": result["msg"]}

@app.get("/rooms")
def rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM hotel_rooms
            ORDER BY room_number
        """)
        rooms = cur.fetchall()
    return rooms

@app.get("/rooms/{id}")
def get_room(id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM hotel_rooms
            WHERE id = %s
        """, (id,))
        room = cur.fetchall()
    return room

@app.post("/bookings")
def create_booking(booking: Booking, guest:dict = Depends(validate_api_key)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO hotel_bookings (
                guest_id,
                room_id,
                datefrom,
                dateto,
                addinfo
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            RETURNING *
        """, (
            booking.guest_id,
            booking.room_id,
            booking.datefrom,
            booking.dateto,
            booking.addinfo
        ))
        new_booking = cur.fetchone()

    return {"msg": "booking created", "booking": new_booking}


#list all bookings
@app.get("/bookings")
def get_bookings(guest: dict = Depends(validate_api_key)):
 print(guest)
 with get_conn() as conn, conn.cursor() as cur:
    cur.execute("""
        SELECT
            hb.id,
            hg.first_name,
            hg.last_name,
            hr.room_number,
            hb.datefrom,
            hb.dateto,
            (hb.dateto::date - hb.datefrom::date) AS nights,
            hr.price,
            (hb.dateto::date - hb.datefrom::date) * hr.price AS total_price,
            hb.addinfo,
            hb.stars
        FROM hotel_bookings hb
        INNER JOIN hotel_guests hg
            ON hb.guest_id = hg.id
        INNER JOIN hotel_rooms hr
            ON hb.room_id = hr.id
        ORDER BY hb.id DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    return rows

@app.put("/bookings/{id}")
def update_booking_stars(id:int, review: BookingStars, guest: dict = Depends(validate_api_key)):
    if review.stars < 1 or review.stars > 5:
        raise HTTPException(status_code=400, detail="Stars must be between 1 and 5")
    
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(""" 
                    UPDATE hotel_bookings
                    SET stars = %s
                    WHERE id = %s
                    AND guest_id = %s
                    RETURNING *
                    """,(review.stars, id, guest['id']))
        update_booking = cur.fetchone()
                    
    if not update_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return{"msg": "review saved", "booking": update_booking}
    

# List all guests
@app.get("/guests")
def get_guests(guest: dict = Depends(validate_api_key)):
 with get_conn() as conn, conn.cursor() as cur:
    cur.execute("""
        SELECT
            hg.id,
            hg.first_name,
            hg.last_name,
            hg.address,
            (
                SELECT COUNT(*)
                FROM hotel_bookings hb
                WHERE hb.guest_id = hg.id
                  AND hb.dateto::date < CURRENT_DATE
            ) AS previous_visits
        FROM hotel_guests hg
        ORDER BY hg.id
    """)
    rows = cur.fetchall()
    return rows

@app.get("/current_guest")
def get_current_guest(guest: dict = Depends(validate_api_key)):
    return {
        "id": guest["id"],
        "first_name": guest["first_name"],
        "last_name": guest["last_name"]
    }

@app.get("/debug/guests")
def debug_guests():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, first_name, last_name, api_key
            FROM hotel_guests
        """)
        return cur.fetchall()