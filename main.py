from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, chat, followup

app = FastAPI(title="Carenova API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/api/auth",    tags=["Auth"])
app.include_router(chat.router,     prefix="/api/chat",    tags=["Chat"])
app.include_router(followup.router, prefix="/api/followup",tags=["Followup"])

@app.get("/")
def root():
    return {"message": "Carenova API is running"}