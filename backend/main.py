from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Algo trading backend is running 🚀"}
