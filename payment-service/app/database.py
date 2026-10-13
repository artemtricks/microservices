from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import settings



engine = create_engine(settings.database_url, echo=True)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: db.close()