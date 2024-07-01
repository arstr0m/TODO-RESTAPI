from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

import Auth.auth
from Data.database import get_db
from Models import models
from Schemas import schemas

router = APIRouter(
    prefix='/icons',
    tags=['Icons']
)


@router.get('/', response_model=list[schemas.IconsBase])
async def get_icons(db: Session = Depends(get_db)):
    try:
        user_icons = db.query(models.Icons).all()
        if user_icons is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Icons not found")
        return user_icons
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.get('/{icons_id}', response_model=schemas.IconsBase)
async def get_icons_by_id(icons_id: int, db: Session = Depends(get_db)):
    try:
        get_icon = db.query(models.Icons).filter(models.Icons.id_icon == icons_id).first()
        if get_icon is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found")
        return get_icon
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.IconsBase)
async def create_icon(new_icon: schemas.IconsBase, db: Session = Depends(get_db)):
    try:
        _new_icon = models.Icons(**new_icon.dict())
        db.add(_new_icon)
        db.commit()
        db.refresh(_new_icon)
        return _new_icon
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


# TODO CHECK THIS, IT IS NOT DELETING PROPERLY ->Solved, it was removed .first() function after db.query, it takes an
#  object not a query that way

@router.delete('/{icon_id}', status_code=status.HTTP_200_OK)
async def delete_icon(icon_id: int, db: Session = Depends(get_db)):
    try:
        deleted_icon = db.query(models.Icons).filter(models.Icons.id_icon == icon_id)
        if deleted_icon is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {icon_id} you requested for does not exist")
        deleted_icon.delete(synchronize_session=False)
        db.commit()
        return {"message": "Icons deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.put('/{icon_id}', response_model=schemas.IconsBase)
def update_icon(_upd_icon: schemas.IconsBase, icon_id: int, db: Session = Depends(get_db)):
    try:
        updated_icon = db.query(models.Icons).filter(models.Icons.id_icon == icon_id).first()
        if updated_icon is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{icon_id} does not exist")
        update_data = _upd_icon.dict()
        for key, value in update_data.items():
            setattr(updated_icon, key, value)
        db.commit()
        return updated_icon
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )
