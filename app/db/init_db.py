from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.core.config import settings

def init_db():
    """
    Initialize the database by creating all tables
    """
    engine = create_engine(
        settings.DATABASE_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Add any initial data here if needed
        pass
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")