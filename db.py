from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5433/random_weather"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

if __name__ == "__main__":
    with engine.connect() as connection:
        print("Database connected!")