from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from app.config import DATABASE_URL


Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    from_address = Column("from", String, nullable=False)
    to_address = Column("to", String, nullable=False)
    type = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    attachments = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.now())
    provider_id = Column(String, nullable=True)
    provider = Column(String, nullable=True)  # optional: sms/email source


assert DATABASE_URL is not None, "DATABASE_URL must be set"
engine = create_engine(DATABASE_URL)


# For dev: create tables if they don't exist
def create_tables():
    Base.metadata.create_all(bind=engine)
