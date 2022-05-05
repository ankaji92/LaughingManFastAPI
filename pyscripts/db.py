from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

def insert_faces(faces):
    SessionClass = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionClass()
    for face in faces:
        face_instance = Face()
        face_instance.st_x = int(face[0])
        face_instance.st_y = int(face[1])
        face_instance.width = int(face[2])
        face_instance.height = int(face[3])
        session.add(face_instance)
    session.commit()
    session.close()
