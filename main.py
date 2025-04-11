from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "Hola desde Railway con FastAPI 🚀"}
