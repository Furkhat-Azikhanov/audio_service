from fastapi import FastAPI

app = FastAPI(title="Audio Service")

@app.get("/")
def read_root():
    return {"message": "Hello World!"}
