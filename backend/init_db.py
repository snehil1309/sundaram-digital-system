import os
import sys

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import init_db

if __name__ == "__main__":
    print("Initializing Database...")
    init_db()
    print("Database initialized successfully at 'database/database.db'!")
