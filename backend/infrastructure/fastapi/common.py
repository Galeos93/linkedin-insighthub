from fastapi import FastAPI, Request, Response, Depends
import uuid


def get_anonymous_user(request: Request, response: Response):
    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            samesite="lax",
            secure=False,  # IMPORTANT: Set to True in production with HTTPS
        )
    print("Session ID:", session_id)

    return session_id
