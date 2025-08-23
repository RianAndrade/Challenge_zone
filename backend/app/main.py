
from fastapi import FastAPI
from app.routes.properties import router as properties_router
from app.routes.reservations import router as reservations_router

app = FastAPI(title="Challenge Zone")
app.include_router(properties_router)
app.include_router(reservations_router) 


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hello, rias"}
