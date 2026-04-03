from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import asyncio

from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
# from api.chat.ai.services import generate_email_message
from api.chat.ai.agents import get_supervisor_agent
from api.chat.ai.schemas import EmailMessageSchema, SupervisorResponse
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
    # results = session.exec(query).fetchall()[:10]
    results = session.exec(query).fetchall()
    return results


# HTTP post -> payload = {"message":"hello world"} -> response = {"message":"hello world", "id":1}
# curl -X POST -d '{"message":"how are you bro"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
# curl -X POST -d '{"message":"how are you bro"}' -H "Content-Type: application/json" https://deploy-ai-agent-beginner-challenge-production.up.railway.app/api/chats/
# curl -X POST -d '{"message":"Give me a brief account on the fall of Rome"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
# curl -X POST -d '{"message":"Give me a brief account on the fall of Rome"}' -H "Content-Type: application/json" https://deploy-ai-agent-beginner-challenge-production.up.railway.app/api/chats/
# curl -X POST -d '{"message":"Give a brief account on the fall of Rome and mail it to seblelivingstone@gmail.com"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
# curl -X POST -d '{"message":"Research and give a brief account on Sadam Husein and mail it to seblelivingstone@gmail.com, just use the tools you have"}' -H "Content-Type: application/json" https://deploy-ai-agent-beginner-challenge-production.up.railway.app/api/chats/


supervisor = get_supervisor_agent()

@router.post("/", response_model=SupervisorResponse)
async def chat_create_message(payload: ChatMessagePayload, session: Session = Depends(get_session)):
    data = payload.model_dump() # pydantic -> dict
    db_obj = ChatMessage.model_validate(data)
    # store data in db
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj) # ensures the id/primary_key is added to the obj instance
    # response = generate_email_message(payload.message)
    msg_data = {
        "messages":[{
            "role":"user",
            "content":f"{payload.message}"
        }]
    }
    result = await asyncio.to_thread(
        supervisor.invoke,
        msg_data
    )
    if not result:
        raise HTTPException(status_code=400, detail="Error with supervisor")
    messages = result.get("messages")
    if not messages:
        raise HTTPException(status_code=400, detail="Error with supervisor")
    return messages[-1]