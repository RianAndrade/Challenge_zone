
from fastapi import FastAPI
from app.routes.properties import router as properties_router
from app.routes.reservations import router as reservations_router

app = FastAPI(title="Challenge Zone")
app.include_router(properties_router)
app.include_router(reservations_router) 

@app.get("/")
def read_root():
    return {"message": "Para acessar o Swagger: http://127.0.0.1:8000/docs#/"}
