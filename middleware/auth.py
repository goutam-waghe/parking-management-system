from fastapi import Request  , responses
from fastapi.responses import JSONResponse
from model import User
from utils.token import verify_token
from sqlalchemy.orm import Session
from database import get_db


async def isAuthenticated(request:Request , call_next):
    try:
        if request.url.path in ["/user/login", "/user/signup"]:
            response = await call_next(request)
            return response
        auth_header = request.headers.get("token")
        token = auth_header.split(" ")[1]
        isLoggedIn = verify_token(token)
        email = isLoggedIn["email"]
        if not isLoggedIn:
            responses.JSONResponse(status_code=401 ,  content={"error": "Invalid token"})
       
        
        request.state.email = email
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}  
        )
   