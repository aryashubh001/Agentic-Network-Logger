import psycopg2
import time
import random
from datetime import datetime
# safe mode connection
DB_HOST = "Paste your host here"
DB_PORT = "Port Number"
DB_USER = "tsdbadmin"
DB_PASS = "Password"
DB_NAME = "tsdb"

def start_agent():
    print("1. Function called...")
    try:
        print(f"2. Connecting to {DB_HOST}...")
        
        # We connect using separate parameters to avoid URL errors
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            dbname=DB_NAME,
            sslmode='require' # Timescale Cloud requires SSL
        )
        cur = conn.cursor()
        print("3. Connected to Timescale Cloud!")

        while True:
            timestamp = datetime.now()
            device = f"device_{random.randint(1, 50)}"
            bytes_sent = random.randint(100, 5000)
            risk = round(random.uniform(0, 10), 2)

            # Insert Query
            query = "INSERT INTO network_logs (time, device_id, bytes_sent, risk_score) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (timestamp, device, bytes_sent, risk))
            conn.commit()
            
            print(f"[{timestamp}] Logged: {device} | Risk: {risk}")
            time.sleep(0.5) 

    except Exception as e:
        print(f"Error: {e}")
        print("HINT: If the password is wrong, go to Timescale Dashboard -> Project Settings -> Reset Password.")

if __name__ == "__main__":

    start_agent()
