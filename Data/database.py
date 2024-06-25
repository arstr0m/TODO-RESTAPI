from urllib.parse import quote_plus
import consts
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

encoded_password = quote_plus(consts.PASSWORD)
SQLALCHEMY_DATABASE_URL = f"postgresql://{consts.USERNAME}:{encoded_password}@{consts.HOST}:{consts.PORT}/{consts.DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
