from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    search_filter: Mapped['SearchFilter'] = relationship(back_populates='user', cascade="all, delete-orphan")
    blacklist: Mapped['BlackList'] = relationship(back_populates='user', cascade="all, delete-orphan")
    token: Mapped['Token'] = relationship(back_populates='user', cascade="all, delete-orphan")


class SearchFilter(Base):
    __tablename__ = 'search_filters'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    resume_id: Mapped[str] = mapped_column(nullable=False)
    key_words: Mapped[str] = mapped_column(nullable=False)
    experience: Mapped[str] = mapped_column(nullable=True)
    area: Mapped[int] = mapped_column(nullable=True)
    period: Mapped[int] = mapped_column(nullable=True)
    schedule: Mapped[str] = mapped_column(nullable=True)
    salary: Mapped[int] = mapped_column(nullable=True)
    search_field: Mapped[str] = mapped_column(nullable=True)
    message: Mapped[str] = mapped_column(nullable=True)
    
    user: Mapped['User'] = relationship(back_populates='search_filter')


class BlackList(Base):
    __tablename__ = 'black_list'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    companies: Mapped[list[str]] = mapped_column(JSONB, nullable=True)
    
    user: Mapped['User'] = relationship(back_populates='blacklist')


class Token(Base):
    __tablename__ = 'tokens'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    access_token: Mapped[str] = mapped_column(nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)
    create_or_update: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    
    user: Mapped['User'] = relationship(back_populates='token')


class UserBlackList(Base):
    __tablename__ = 'user_blacklist'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    user_first_name: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
