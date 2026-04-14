from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

create_schema()

class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date
    addinfo: Optional[str] = None

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

@app.get("/bookings")
def get_bookings():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT
                hb.id,
                hb.guest_id,
                hb.room_id,
                hb.datefrom,
                hb.dateto,
                hb.addinfo,
                hr.room_number
            FROM hotel_bookings hb
            JOIN hotel_rooms hr ON hb.room_id = hr.id
            ORDER BY hb.datefrom, hb.dateto
        """)
        bookings = cur.fetchall()
    return bookings

@app.post("/bookings")
def create_booking(booking: Booking):
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

@app.on_event("startup")
def startup():
    create_schema()