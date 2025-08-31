from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# هنا حط رابط قاعدة البيانات
# لو شغال بـ SQLite:
SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"

# لو PostgreSQL أو MySQL:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

Base = declarative_base()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # مطلوب فقط مع SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
