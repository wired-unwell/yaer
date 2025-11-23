import psycopg2

DB_CONFIG = {
    "dbname": "workout_tracker",
    "user": "wt_admin",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

def initialize_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  workout_tracker.exercises (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        egroup VARCHAR(255),
        muscle VARCHAR(255)[],
        equipment VARCHAR(255)[],
        intensity INTEGER,
        difficulty INTEGER,
        external_url VARCHAR(255)
    );
    """)
    # conn.commit()
    # cursor.close()
    # conn.close()

def seed_():
    try:
        pass
    except:
        pass
    finally:
        pass

def main():
    seed_exercises()

initialize_table()
    
# conn = psycopg2.connect(**DB_CONFIG)
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM workout_tracker.exercises")
