from datetime import timedelta
from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

import Auth.auth
import Utils.validation
import consts
from Data.database import get_db
from Models import models
from Schemas import schemas

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/all', response_model=List[schemas.GetUser])
async def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(models.Users).all()
        return users

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )


# TODO CHECK THIS BECAUSE IT IS NOT TAKING THE BEARER TOKEN FROM AUTH

@router.get("/me", response_model=schemas.GetUser)
async def read_users_me(current_user: schemas.GetUser = Depends(Auth.auth.get_current_user)):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get('/email/{email}')
async def get_user_by_user_email(email: str, db: Session = Depends(get_db)):
    try:
        return db.query(models.Users).filter(models.Users.email == email).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )


@router.get("/id/{id_user}", response_model=schemas.GetUser)
def get_user_by_its_id(id_user: int, db: Session = Depends(get_db)):
    try:
        print(id_user)
        found_user = db.query(models.Users).filter(models.Users.id_user == id_user).first()
        if found_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"The id: {id_user} you requested for does not exist")
        return found_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )


# todo logout
@router.post("/logout")
async def logout(db: Session = Depends(get_db)):
    pass


# TODO cypher password
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUser)
async def create_user(new_user: schemas.CreateUser, db: Session = Depends(get_db)):
    try:
        if db.query(models.Users).filter(models.Users.username == new_user.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        if db.query(models.Users).filter(models.Users.username == new_user.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        # TODO IT WAS REMOVED EMAIL VALIDATION
        if Utils.validation.word_length(8, 16, new_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="not a valid password"
            )
        new_us = models.Users(**new_user.dict())
        db.add(new_us)
        db.commit()
        db.refresh(new_us)
        return new_us
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )


@router.post("/login", response_model=schemas.Token, status_code=status.HTTP_202_ACCEPTED)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = Auth.auth.authenticate_user(form_data.username, form_data.password, db)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=consts.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await Auth.auth.create_access_token(
            data={"sub": str(user.username)},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect username or password {e}"
        )


@router.delete('/id/{id_user}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id_user: int, db: Session = Depends(get_db)):
    try:
        deleted_user = db.query(models.Users).filter(models.Users.id_user == id_user)
        if deleted_user.first() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id_user} you requested for does not exist")
        deleted_user.delete(synchronize_session=False)
        db.commit()
        return {"message": "Icons deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )


@router.put('/id/{id_user}', response_model=schemas.UpdateUser)
def update_user(upd_image: schemas.UpdateUser, id_user: int, db: Session = Depends(get_db)):
    try:
        updated_user = db.query(models.Users).filter(models.Users.id_user == id_user)
        if updated_user.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id_user} does not exist")
        updated_user.update(upd_image.dict(), synchronize_session=False)
        db.commit()
        return updated_user.first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )
