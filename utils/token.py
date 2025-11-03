from jose import JWTError, jwt
from datetime import datetime, timedelta
import os 
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# Encode
def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


# Decode
def verify_token(token:str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except JWTError:
        return {
            "message":"invaild token"
        }

