from sqlalchemy.orm import sessionmaker
from app.models.message import Message, engine
from app.schemas.message import MessageSchema

SessionLocal = sessionmaker(bind=engine)


def save_message(payload: MessageSchema) -> Message:
    with SessionLocal() as db:
        message = Message(
            from_address=payload.from_,
            to_address=payload.to,
            type=payload.type,
            attachments=payload.attachments,
            timestamp=payload.timestamp,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message


def get_all_messages() -> list[Message]:
    with SessionLocal() as db:
        return db.query(Message).order_by(Message.timestamp.desc()).all()
