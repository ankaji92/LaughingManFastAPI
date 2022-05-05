from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/face_location.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

Base = declarative_base()

class Face(Base):
    __tablename__ = "face"
    id = Column(Integer, primary_key=True)
    st_x = Column(Integer)
    st_y = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)

Base.metadata.create_all(bind=engine)