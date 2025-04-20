from fastapi import FastAPI, Request
from pydantic import BaseModel
from order import order

app = FastAPI()

class OrderRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"msg": "running!"}

@app.post("/order")
def process_order(req: OrderRequest):
    result = order(req.message)
    return {"result": result}
