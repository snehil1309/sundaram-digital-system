from models.database import SessionLocal, Order, PointsHistory

def truncate_tables():
    db = SessionLocal()
    try:
        db.query(Order).delete()
        db.query(PointsHistory).delete()
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    truncate_tables()
    print("Orders and PointsHistory tables truncated.")
