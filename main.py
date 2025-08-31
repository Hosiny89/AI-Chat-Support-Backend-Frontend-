from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
from routers import chat

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://congenial-fiesta-9vqxqx779rcp6r6-5173.app.github.dev",  # React على Codespaces
        "https://congenial-fiesta-9vqxqx779rcp6r6-8000.app.github.dev", # Backend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# تسجيل الرواتر
app.include_router(chat.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Server is running 🚀"}

    https://github.com/Hosiny89/AI-Chat-Support-Mini-Chatgpt-