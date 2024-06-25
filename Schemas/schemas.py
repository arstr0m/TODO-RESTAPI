import string
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    id_user: Optional[int] = None
    username: str
    password: str

    class Config:
        from_attributes = True


class GetUser(UserBase):
    email: str

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    email: str
    first_name: str
    last_name: str
    status: Optional[str] = "ACT"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DeleteUser(UserBase):
    class Config:
        from_attributes = True


class UpdateEmail(UserBase):
    email: str

    class Config:
        from_attributes = True


class UpdateUser(UserBase):
    class Config:
        from_attributes = True


class IconsBase(BaseModel):
    id_icon: int
    ico: str
    created_at: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    id_task: int
    id_user: int
    id_icon: Optional[int] = None
    title: str
    detail: Optional[str] = None

    class Config:
        from_attributes = True


class CreateTask(TaskBase):
    added_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UpdateTask(TaskBase):
    isFinished: bool
    status: str

    class Config:
        from_attributes = True
