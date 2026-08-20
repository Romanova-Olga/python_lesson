from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class TeacherTable(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=False)

# Строка подключения (ЗАМЕНИТЕ ПАРОЛЬ НА СВОЙ!)
DB_URL = "postgresql://postgres:KarameLLublu@localhost:5432/postgres"

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
