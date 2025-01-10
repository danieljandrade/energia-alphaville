from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

DB_NAME = 'database/energia_alphaville.db'

def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)  # Permitir uso em múltiplas threads
    try:
        yield conn
    finally:
        conn.close()

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="As senhas não coincidem.")
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres.")

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, False))
        db.commit()
        return RedirectResponse(url="/?msg=success", status_code=303)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Usuário já existe.")
