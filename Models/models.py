from typing import List

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from Data.database import Base

class Users(Base):
    __tablename__ = "users"
    id_user: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(40), nullable=False)
    username = Column(String(30), nullable=False, index=True)
    email = Column(String(50), nullable=False, index=True)
    password = Column(String(200), nullable=False, server_default='FALSE')
    status = Column(String(3), nullable=False, server_default='ACT')

    tasks_users: Mapped[List["TaskUsers"]] = relationship("TasksUsers", back_populates="users")


class Icons(Base):
    __tablename__ = 'icons'
    id_icon: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    added_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    ico = Column(String(1), nullable=False)
    status = Column(String(3), nullable=False, server_default='ACT')

    tasks_users: Mapped[List["TasksUsers"]] = relationship("TasksUsers", back_populates="icons")


class TasksUsers(Base):
    __tablename__ = 'tasks_users'
    id_task: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id_user"), primary_key=True)
    id_icon: Mapped[int] = mapped_column(ForeignKey("icons.id_icon"), primary_key=True)
    title = Column(String(250), nullable=False)
    detail = Column(String(250), nullable=True)
    is_finished = Column(Boolean, nullable=False, default=True)
    added_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    ends_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=True)
    status = Column(String(3), nullable=False, server_default='ACT')

    users: Mapped["Users"] = relationship("Users", back_populates="tasks_users")
    image: Mapped["Icons"] = relationship("Image", back_populates="tasks_users")




