from fastapi import APIRouter
import shutil
import datetime
import os

router = APIRouter()

@router.post("/backup")
def backup_database():
    try:
        source_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", "database.db"))
        backup_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backup"))
        
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"database_backup_{timestamp}.db")
        
        shutil.copy2(source_db, backup_file)
        
        return {"message": "Backup successful", "backup_file": f"database_backup_{timestamp}.db"}
    except Exception as e:
        return {"error": str(e)}
