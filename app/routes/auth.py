from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

DB_NAME = 'database/energia_alphaville.db'

def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)  # Correção aplicada
    try:
        yield conn
    finally:
        conn.close()

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    if result:
        return RedirectResponse(url="/dashboard", status_code=303)  # Redireciona para uma página de sucesso
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
