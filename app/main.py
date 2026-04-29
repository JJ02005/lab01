from fastapi import FastAPI
from app.routers.books import books_router

# Creiamo l'istanza principale
app = FastAPI()

# Colleghiamo il router dei libri
app.include_router(books_router)

@app.get("/")
def root():
    return {"message": "Server attivo! Vai su /docs per testare le API"}