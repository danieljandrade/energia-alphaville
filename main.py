from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DB_NAME = 'energia_alphaville.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        conn.commit()

init_db()

def get_db():
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    finally:
        conn.close()

class User(BaseModel):
    username: str
    password: str
    is_admin: bool = False

@app.post("/register")
def register_user(user: User, db: sqlite3.Connection = Depends(get_db)):
    try:
        db.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                   (user.username, user.password, user.is_admin))
        db.commit()
        return {"message": "Usuário cadastrado com sucesso!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Usuário já existe.")

@app.post("/login")
def login(user: User, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                   (user.username, user.password))
    result = cursor.fetchone()
    if result:
        return {"message": "Login realizado com sucesso!"}
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
