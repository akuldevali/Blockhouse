from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.websocket import manager
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from app.database import init_db

init_db()  # Ensure tables exist
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Replace "*" with specific frontend URLs in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    if order.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero")
    
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")
    
    if order.order_type not in {"BUY", "SELL"}:
        raise HTTPException(status_code=400, detail="Invalid order type. Must be either 'BUY' or 'SELL'.")

    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    await manager.send_update(db_order)  

    return db_order


@app.get("/orders/", response_model=list[schemas.Order])
def read_orders( limit: int = 100, db: Session = Depends(database.get_db)):

    if limit <=0:
        raise HTTPException(status_code=400, detail="Limit must be greater then 0")

    orders = db.query(models.Order).order_by(models.Order.id.desc()).limit(limit).all()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Client trying to connect...")
    await manager.connect(websocket)
    print("Client connected.")
    try:
        while True:
            data = await websocket.receive_text() if await websocket.receive_text() else None
            if data:
                print("Received:", data)
    except WebSocketDisconnect:
        print("Client disconnected")
        manager.disconnect(websocket)

@app.get("/")
def root():
    return {"Hello": "World"}