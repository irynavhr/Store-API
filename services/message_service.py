from sqlalchemy.orm import Session

from models.message import Message
from models.user import User
from schemas.message import MessageCreate


def create_message(
    db: Session,
    current_user: User,
    message_data: MessageCreate
):

    message = Message(
        subject=message_data.subject,
        message=message_data.message,
        user_id=current_user.id
    )

    db.add(message)

    db.commit()
    db.refresh(message)

    return message


# GET ALL MESSAGES (ADMIN ONLY)
def get_all_messages(db: Session):

    return db.query(Message).all()