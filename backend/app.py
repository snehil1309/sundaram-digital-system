from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import customers, orders, points, reports, backup, auth

app = FastAPI(title="Sundaram Digital Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(customers.router, prefix="/api", tags=["Customers"])
app.include_router(orders.router, prefix="/api", tags=["Orders"])
app.include_router(points.router, prefix="/api", tags=["Points"])
app.include_router(reports.router, prefix="/api", tags=["Reports"])
app.include_router(backup.router, prefix="/api", tags=["Backup"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Sundaram Digital API"}
