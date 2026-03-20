from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from rag import rag_answer

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []


class ChatResponse(BaseModel):
    possible_conditions: list
    explanation: list
    home_care_tips: list
    when_to_see_doctor: list
    disclaimer: str


def get_token_from_request(request: Request):
    """Extract Bearer token from Authorization header manually."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None


def verify_token(token: str):
    """Verify token — allows demo tokens, real Firebase tokens, or no token in dev."""

    # ✅ No token at all — allow in demo/dev mode
    if not token:
        return {"uid": "dev_user", "email": "dev@carenova.test"}

    # ✅ Demo token — allow directly
    if token.startswith("demo_token_"):
        return {"uid": "demo_user", "email": "demo@carenova.test"}

    # Real Firebase token verification
    try:
        from firebase_admin import auth as firebase_auth
        decoded = firebase_auth.verify_id_token(token)
        return decoded
    except ImportError:
        raise HTTPException(status_code=503, detail="Firebase not configured on server.")
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized. Please login again.")


@router.post("/message", response_model=ChatResponse)
async def chat_message(request: Request, body: ChatRequest):
    # Extract and verify token
    token = get_token_from_request(request)
    verify_token(token)  # raises HTTPException if invalid

    user_message = body.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        result = rag_answer(user_message)
        return ChatResponse(
            possible_conditions=result.get("possible_conditions", []),
            explanation=result.get("explanation", []),
            home_care_tips=result.get("home_care_tips", []),
            when_to_see_doctor=result.get("when_to_see_doctor", []),
            disclaimer=result.get("disclaimer", "This is not a medical diagnosis. Consult a healthcare professional.")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {str(e)}")


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "Carenova Chat API"}