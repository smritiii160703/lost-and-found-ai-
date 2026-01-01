from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)           # lost / found
    title = Column(String)
    description = Column(String)
    location = Column(String)
    image_path = Column(String)
    contact = Column(String)
    resolved = Column(Boolean, default=False)

