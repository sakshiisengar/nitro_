from fastapi import FastAPI
from. import models, database

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the File Parser API"}
# Add import and endpoints implementations
