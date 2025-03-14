from datetime import datetime
import pytz
import json
from route import Route
from ETA import get_eta
from helping_functions import eta_to_mins
import pg8000
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

DB_USER= "postgres",
DB_PASSWORD = "xWuUhObXjE7A0mGL",
DB_HOST = "db.ssarfaveqegyxubkgtro.supabase.co",
DB_PORT = "5432",
DB_NAME = "postgres"

def get_db_connection():
    return pg8000.connect(
        user="postgres",
        password="xWuUhObXjE7A0mGL",
        host="db.ssarfaveqegyxubkgtro.supabase.co",
        port=int("5432"),
        database="postgres"
    )

def scrape():
    gmt_hour = datetime.now(pytz.timezone('GMT')).hour

    # Load jobs file dynamically based on current hour
    with open(f"jobs_JSON/jobs{gmt_hour}.json", "r") as f:
        routes = [Route.from_dict(route) for route in json.load(f)]

    for r in routes:
        url = r.url
        eta = get_eta(url)  # Function to get ETA (assumed to exist)
        eta_mins = eta_to_mins(eta)  # Convert ETA to minutes
        route_id = r.route_id

        # Insert the values into the database
        insert_eta(route_id, eta_mins)

# Function to insert ETA into database
def insert_eta(route_id, eta_mins):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert query with conflict handling
        cursor.execute(
            """
            INSERT INTO "Routes" ("Route_ID", "ETA") 
            VALUES (%s, %s)
            ON CONFLICT ("Route_ID") 
            DO UPDATE SET "ETA" = EXCLUDED."ETA";
            """,
            (route_id, eta_mins)
        )

        conn.commit()
        cursor.close()
        conn.close()

        print(f"✅ ETA {eta_mins} minutes inserted for Route_ID {route_id} successfully!")

    except Exception as e:
        print(f"❌ Error inserting ETA: {e}")

# Flask route to add ETA via API
@app.route('/add_eta', methods=['POST'])
def add_eta():
    data = request.json  # Extract JSON request data

    # Ensure required fields exist in request
    if 'Route_ID' not in data or 'ETA' not in data:
        return jsonify({"error": "Missing Route_ID or ETA"}), 400

    try:
        insert_eta(data['Route_ID'], data['ETA'])
        return jsonify({"message": f"ETA {data['ETA']} inserted for Route_ID {data['Route_ID']} successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app (Only required if running independently)
if __name__ == '__main__':
    #ghjh
    scrape()