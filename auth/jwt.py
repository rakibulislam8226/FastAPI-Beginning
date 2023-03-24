from logging import currentframe
from os import access, stat
from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List
from fastapi_jwt_auth import AuthJWT
from pydantic.networks import url_regex
from starlette.status import HTTP_401_UNAUTHORIZED
from auth.schemas import User, UserLogin
from src.database import Base, engine, SessionLocal
from auth import models

app=FastAPI()

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


users=[]

#create a user
@app.post('/signup')
async def create_user(user:User, session=Depends(get_session)):
    new_user = models.User(email=user.email, username=user.username, hashed_password=user.hashed_password)
    if new_user:
        session.add(new_user)
        session.commit()
        session.refresh
        return new_user
    else:
        raise HTTPException(status_code=404, detail="Item not found")


#getting all users
@app.get('/users',response_model=List[User])
def get_users(session=Depends(get_session)):
    all_users = session.query(models.User).all()
    return all_users


#getting one user
@app.get('/user/{id}')
def get_user(id:int, session=Depends(get_session)):
    user = session.query(models.User).get(id)
    return user


@app.post('/login', description="Login api")
def login(user:UserLogin, Authorize:AuthJWT=Depends(), session=Depends(get_session)):
    all_users = session.query(models.User).all()
    for u in all_users:
        if (user.username == u.username) and (user.hashed_password == u.hashed_password):
            access_token=Authorize.create_access_token(subject=user.username)
            refresh_token=Authorize.create_refresh_token(subject=user.username)
            return {"access_token":access_token,"refresh_token":refresh_token}
        # else:
        #     # raise HTTPException(status_code='401',detail="Invalid username or password")
        # return {"message": "Invalid username or password"}
    return {"message": "Invalid username or password"}


@app.get('/protected')
def get_logged_in_user(Authorize:AuthJWT=Depends(), session=Depends(get_session)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    current_user=Authorize.get_jwt_subject()
    return {"current_user":current_user}


@app.get('/new_token')
def create_new_token(Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    current_user=Authorize.get_jwt_subject()

    access_token=Authorize.create_access_token(subject=current_user)

    return {"new_access_token":access_token}


@app.post('/fresh_login')
def fresh_login(user:UserLogin,Authorize:AuthJWT=Depends()):
    for u in users:
        if (u["username"]==user.username) and (u["password"]==user.password):
            fresh_token=Authorize.create_access_token(subject=user.username,fresh=True)

            return {"fresh_token":fresh_token}

    
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED,detail="Invalid Username or Password")



@app.get('/fresh_url')
def get_user(Authorize:AuthJWT=Depends()):
    try:
        Authorize.fresh_jwt_required()
    except Exception as e:
        raise HTTPException(status=HTTP_401_UNAUTHORIZED,detail="Invalid Token")

    current_user=Authorize.get_jwt_subject()

    return {"current_user":current_user}
