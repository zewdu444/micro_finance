from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from  routes.api import api_router

app = FastAPI(
  title= "Microfinance API",
  description= "API for Microfinance",
  version= "1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
  return {"message": "Hello World"}
