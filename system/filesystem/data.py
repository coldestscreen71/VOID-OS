import sqlite3
from system.errorcontrol.error import er


conn = sqlite3.connect("system/filesystem/data.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS DATA (
    loc TEXT PRIMARY KEY,
    data TEXT NOT NULL
)
""")
conn.commit()

def add_data(loc,data):
    try:
        cur.execute(
            "INSERT INTO DATA (loc,data) VALUES (?, ?)",
            (loc,data)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        er("already exists")
        

def get_data(loc):
    cur.execute(
        "SELECT data FROM DATA WHERE loc=?",
        (loc,)
    )
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
      
def update_data(loc, data):
    cur.execute(
        "UPDATE DATA SET data=? WHERE loc=?",
        (data, loc)
    )
    conn.commit()
    
def delete_data(loc):
    cur.execute("DELETE FROM DATA WHERE loc=?", (loc,))
    conn.commit()