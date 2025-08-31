from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import ollama

router = APIRouter()

class ChatRequest(BaseModel):
     user_message: str

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    try:
        def generate():
            for chunk in ollama.chat(
                model="gemma:2b",
                messages=[{"role": "user", "content": request.user_message}],
                stream=True,  # خلي الرد ييجي chunks
                options={"timeout": 60}
            ):
                if "message" in chunk and "content" in chunk["message"]:
                    yield chunk["message"]["content"]

        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))