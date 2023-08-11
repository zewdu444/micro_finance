from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from  routes.api import api_router

app = FastAPI(
  title= "Microfinance API",
  description= "API for Microfinance",
  version= "1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
  return {"message": "Welcome to Microfinance API please visit /docs for documentation"}
