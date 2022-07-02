from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Text(Base):
    __tablename__ = "msgs"
    id = Column(Integer, primary_key=True, index=True)
    msg = Column(String)