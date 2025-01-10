from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth, register  # Adicionado

app = FastAPI()

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rotas
app.include_router(auth.router)
app.include_router(register.router)
