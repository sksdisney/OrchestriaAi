import os
from sqlmodel import SQLModel, create_engine, Session

# 'db' is the service name from your docker-compose.yml
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)

# This creates the table if it doesn't exist
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
