import os
import psycopg
from psycopg import rows

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

def get_conn():
  return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=rows.dict_row)

def create_schema():
   with get_conn() as conn, conn.cursor() as cur:
        # Create the schema
            cur.execute("""
                -- Lägg till pgcrypto
                CREATE EXTENSION IF NOT EXISTS pgcrypto;
                -- sample parent table
                CREATE TABLE IF NOT EXISTS hotel_rooms (
                    id SERIAL PRIMARY KEY,
                    room_number INT NOT NULL,
                    room_type VARCHAR NOT NULL,
                    price INT NOT NULL
                );
                 
                ---------  
                 -- guests
                ---------
                CREATE TABLE IF NOT EXISTS hotel_guests (
                    id SERIAL PRIMARY KEY, -- primary key,
                    first_name  VARCHAR NOT NULL,
                    last_name  VARCHAR NOT NULL,
                    created_at TIMESTAMP DEFAULT now(),
                    address VARCHAR
                );
               -- add columns
                --  ALTER TABLE hotel_guests  created_at TIMESTAMP DEFAULT now();
                ALTER TABLE hotel_guests ADD COLUMN IF NOT EXISTS api_key VARCHAR default   encode(gen_random_bytes(32), 'hex');
                
                 ---------  
                 -- bookings
                ---------
                -- bookings
                CREATE TABLE IF NOT EXISTS hotel_bookings (
                  id SERIAL PRIMARY KEY,
                  guest_id INT NOT NULL REFERENCES hotel_guests(id), -- foreign key
                  room_id INT NOT NULL REFERENCES hotel_rooms(id),
                  datefrom DATE DEFAULT now() NOT NULL,
                  dateto DATE NOT NULL,
                  addinfo VARCHAR
                  );
                  
                  -- add columns
                  -- man kan sätta default också senare
                  -- ALTER TABLE hotel_bookings  datefrom  DEFAULT now();
                  -- lägg till främmande nyckel senare:
                  -- ADD CONSTRAINT hotel_guest_id_key FOREIGN KEY (guest_id) REFERENCES
                  
                  ALTER TABLE hotel_bookings
                  ADD COLUMN IF NOT EXISTS stars INT;
                 
            """)