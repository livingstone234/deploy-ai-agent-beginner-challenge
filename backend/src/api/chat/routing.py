from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
from api.chat.ai.services import genearte_email_message
from api.chat.ai.schemas import EmailMessageSchema
from ..db import get_session

router = APIRouter(prefix="/api/chats")

@router.get("/")
async def chat_health():
    return {"status":"ok"}

# /api/chats/recent/
# curl http://localhost:8080/api/chats/recent/
# curl https://deploy-ai-agent-beginner-challenge-production.up.railway.app/api/chats/recent/
@router.get("/recent/", response_model=List[ChatMessageListItem])
async def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage) # sql -> query
    results = session.exec(query).fetchall()[:10]
    return results


# HTTP post -> payload = {"message":"hello world"} -> response = {"message":"hello world", "id":1}
# curl -X POST -d '{"message":"how are you bro"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
# curl -X POST -d '{"message":"how are you bro"}' -H "Content-Type: application/json" https://deploy-ai-agent-beginner-challenge-production.up.railway.app/api/chats/
# curl -X POST -d '{"message":"Give me a brief account on the fall of Rome"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
@router.post("/", response_model=EmailMessageSchema)
async def chat_create_message(payload: ChatMessagePayload, session: Session = Depends(get_session)):
    data = payload.model_dump() # pydantic -> dict
    db_obj = ChatMessage.model_validate(data)
    # store data in db
    session.add(db_obj)
    session.commit()
    # session.refresh(db_obj) # ensures the id/primary_key is added to the obj instance
    response = genearte_email_message(payload.message)
    return response