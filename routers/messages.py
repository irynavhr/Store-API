from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db

from core.dependencies import get_current_user, is_it_admin
from models.user import User
from services import message_service
from schemas.message import MessageCreate, MessageResponse


router = APIRouter(
    prefix="/messages",
    tags=["Contact us"]
)


@router.post("/", response_model=MessageResponse)
def create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return message_service.create_message(db, current_user, message_data)

@router.get("/", response_model=list[MessageResponse])
def get_all_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(is_it_admin)
):

    return message_service.get_all_messages(db)