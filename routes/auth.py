from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

# Only initialize Firebase Admin if service account file exists
# During testing/demo mode, this is skipped entirely
firebase_initialized = False

try:
    import firebase_admin
    from firebase_admin import credentials, auth as firebase_auth

    if not firebase_admin._apps:
        service_account_path = os.getenv(
            "FIREBASE_SERVICE_ACCOUNT_PATH",
            "firebase_service_account.json"
        )
        if os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            firebase_initialized = True
            print("✅ Firebase Admin initialized successfully.")
        else:
            print("⚠️  firebase_service_account.json not found. Running in demo mode.")
    else:
        firebase_initialized = True

except Exception as e:
    print(f"⚠️  Firebase Admin init skipped: {e}")


class TokenRequest(BaseModel):
    id_token: str


@router.post("/verify-token")
async def verify_token(request: TokenRequest):
    """
    Verifies Firebase ID token after magic link authentication.
    In demo mode (token starts with 'demo_token_'), skips Firebase verification.
    """

    # ✅ Demo mode bypass — allow demo tokens without Firebase
    if request.id_token.startswith("demo_token_"):
        return {
            "success": True,
            "uid": "demo_user",
            "email": "demo@carenova.test",
            "message": "Demo authentication successful"
        }

    # Real Firebase verification
    if not firebase_initialized:
        raise HTTPException(
            status_code=503,
            detail="Firebase not configured. Use Demo Login for testing."
        )

    try:
        from firebase_admin import auth as firebase_auth
        decoded_token = firebase_auth.verify_id_token(request.id_token)
        return {
            "success": True,
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email", ""),
            "message": "Authentication successful"
        }

    except firebase_auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token has expired. Please login again.")
    except firebase_auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid token. Authentication failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")