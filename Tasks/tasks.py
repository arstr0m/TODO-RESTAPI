from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

import Auth.auth
from Data.database import get_db
from Models import models
from Schemas import schemas

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@router.get('/', response_model=list[schemas.TaskBase])
async def get_tasks(db: Session = Depends(get_db), user: schemas.UserBase = Depends(Auth.auth.get_current_user)):
    try:
        user_task = db.query(models.TasksUsers).filter_by(id_user=user.id_user).all()
        if user_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found")
        return user_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.get('/{task_id}', response_model=schemas.TaskBase)
async def get_task_by_id(db: Session = Depends(get_db), user: schemas.UserBase = Depends(Auth.auth.get_current_user)):
    try:
        user_task = db.query(models.TasksUsers).filter_by(id_user=user.id_user).first()
        if user_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found")
        return user_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreateTask)
async def create_task(post_posts: schemas.CreateTask, db: Session = Depends(get_db),
                      user: schemas.UserBase = Depends(Auth.auth.get_current_user)):
    try:
        new_task = models.TasksUsers(**post_posts.dict())
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.delete('/{task_id}', status_code=status.HTTP_200_OK)
async def delete_task(task_id: int, db: Session = Depends(get_db),
                      user: schemas.UserBase = Depends(Auth.auth.get_current_user)):
    try:
        deleted_task = db.query(models.TasksUsers).filter(
            models.TasksUsers.id_task == task_id,
            models.TasksUsers.id_user == user.id_user
        ).first()
        if deleted_task is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {task_id} you requested for does not exist")
        db.delete(deleted_task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error " + str(e))
    except AttributeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad Request " + str(e))


@router.put('/{task_id}', response_model=schemas.CreateTask)
def update_task(upd_task: schemas.CreateTask, task_id: int, db: Session = Depends(get_db),
                user: schemas.UserBase = Depends(Auth.auth.get_current_user)):
    try:
        updated_task = db.query(models.TasksUsers).filter(models.TasksUsers.id_task == task_id,
                                                          models.TasksUsers.id_user == user.id_user).first()
        if updated_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{task_id} does not exist")
        db.query(models.TasksUsers).filter_by(id_task=task_id, id_user=user.id_user).update(upd_task.dict())
        db.commit()
        return updated_task
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error " + str(e))
    except AttributeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad Request " + str(e))
