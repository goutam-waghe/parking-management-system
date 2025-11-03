from fastapi import APIRouter, Depends  , status , HTTPException  ,Request
from pydantic import BaseModel , EmailStr 
from sqlalchemy.orm import Session 
from database import get_db
from model import User
from utils.hashPassword import hashPassword , verify_password
from utils.token import create_token
from typing import Optional 
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/user",       
    tags=["User"],        
)




class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone:str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name:  Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def UserSignup(userData:UserCreate , db:Session = Depends(get_db)):
    # check if user already exits
    userExits = db.query(User).filter(User.email == userData.email).first()
    if (userExits) :
        raise HTTPException(
             status_code=status.HTTP_409_CONFLICT ,
             detail="Email already registered"
        )
    # hash password
    hashedpwd= hashPassword(userData.password)
    print(hashedpwd)
    new_user = User(
      name = userData.name ,
      email = userData.email ,
      phone = userData.phone ,
      password =  hashedpwd
    )
    db.add(new_user)
    db.commit()   
    db.refresh(new_user) 
    return {
        "message":"user registered" ,
        "user":new_user
    }

@router.post("/login")
def UserLogin(userData:UserLogin , db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == userData.email).first()
    if not user:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password"
        )
    
    isTrue = verify_password(userData.password , user.password)
    if not isTrue :
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password"
        )
    
    token = create_token({"email":userData.email})
    print(token)

    return {
        "message":"user loggedin" ,
        "token":token
    }

@router.get("/all")
def getAllusers(db:Session = Depends(get_db)):
    all_users = db.query(User).all()
    return {
        "messaage":"all users fetched" ,
        "user":all_users
    }

@router.get("/profile")
def UserProfile( request: Request , db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.state.email)
    return {
        "message":"profile fetched" ,
        "user":user 
    }

@router.put("/edit-profile")
def UserEditProfile(request: Request , userData:UserUpdate , db:Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == request.state.email)

        if(userData.name):
            user.name = userData.name
        if(userData.email):
            user.email = userData.email
        if(userData.phone):
            user.phone = userData.phone

        db.commit()
        db.refresh(user)
        return {
            "message":"update successfully" ,
        }
    except Exception as e:
         return JSONResponse(
            status_code=500,
            content={"error": str(e)}  
        )


@router.delete("/delete")
def UserAccountDelete(request: Request , db:Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == request.state.email)
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
         return JSONResponse(
            status_code=500,
            content={"error": str(e)}  
        )




