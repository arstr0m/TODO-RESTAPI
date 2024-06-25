from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette import status

import consts
from Data.database import get_db
from Models import models
from Schemas import schemas

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/all/{API_KEY}', response_model=List[schemas.GetUser])
async def get_all_users(API_KEY: str, db: Session = Depends(get_db)):
    try:
        if consts.API_KEY == API_KEY:
            users = db.query(models.Users).all()
            return users
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"NOT ALLOWED"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUser)
async def create_user(new_user: schemas.CreateUser, db: Session = Depends(get_db)):
    try:
        new_us = models.Users(**new_user.dict())
        db.add(new_us)
        db.commit()
        db.refresh(new_us)
        return [new_us]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )


@router.get('/{id_user}', response_model=schemas.GetUser, status_code=status.HTTP_200_OK)
def get_image_by_id(id_user: int, db: Session = Depends(get_db)):
    try:
        get_user = db.query(models.Users).filter(models.Users.id_user == id_user).first()
        if get_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id_user} you requested for does not exist")
        return get_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )


@router.delete('/{id_user}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(id_user: int, db: Session = Depends(get_db)):
    try:
        deleted_user = db.query(models.Users).filter(models.Users.id_user == id_user)
        if deleted_user.first() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id_user} you requested for does not exist")
        deleted_user.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        )


@router.put('/upd_user/{id_user}', response_model=schemas.UpdateUser)
def update_image(upd_image: schemas.UpdateUser, id_user: int, db: Session = Depends(get_db)):
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


@router.put('/upd_email/{id_user}', response_model=schemas.UpdateEmail)
def update_image(upd_image: schemas.UpdateEmail, id_user: int, db: Session = Depends(get_db)):
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
