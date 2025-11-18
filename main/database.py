import databases
import sqlalchemy
from sqlalchemy import create_engine

# SQLite URL - data will be stored in a file named sqlite.db
DATABASE_URL = "sqlite:///sqlite.db"

# Create database connection
database = databases.Database(DATABASE_URL)

# Create metadata instance
metadata = sqlalchemy.MetaData()

# Create engine instance
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})