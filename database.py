from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Database_url = "sqlite:///habitrpg.db"

engine = create_engine(Database_url,connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)

base = declarative_base()