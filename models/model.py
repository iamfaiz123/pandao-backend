from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, Enum , DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import Enum as PYENUM
from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func

Base = declarative_base()





class User(Base):
    __tablename__ = 'users'
    name: Mapped[str] = Column(String)
    public_address: Mapped[str] = Column(String(256), primary_key=True)
    last_login: Mapped[DateTime] = Column(DateTime, default=func.now())
    usermetadata: Mapped["UserMetaData"] = relationship("UserMetaData", back_populates="user")


class UserMetaData(Base):
    __tablename__ = 'user_meta_data'
    user_address: Mapped[str] = Column(String, ForeignKey('users.public_address'), primary_key=True)
    about: Mapped[str] = Column(String)
    image_url: Mapped[str] = Column(String)
    user: Mapped["User"] = relationship("User", back_populates="usermetadata")


class UserActivity(Base):
    __tablename__ = 'user_activity'
    transaction_id: Mapped[str] = Column(String, primary_key=True)
    # this contains a basic info about a user transaction in the DAO
    transaction_info: Mapped[str] = Column(String)
    user_address: Mapped[str] = Column(String, ForeignKey('users.public_address'))


class BluePrint(Base):
    __tablename__ = 'blueprint'
    slug: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(DECIMAL)
    package_addr = Column(String, nullable=False)

    # define relationships
    terms: Mapped[list["BluePrintTerms"]] = relationship("BluePrintTerms", back_populates="blueprint")






class BluePrintTerms(Base):
    __tablename__ = 'blueprint_terms'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    term: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    blueprint_slug: Mapped[str] = mapped_column(ForeignKey("blueprint.slug"))
    blueprint: Mapped["BluePrint"] = relationship("BluePrint", back_populates="terms")





class Community(Base):
    __tablename__ = 'community'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(128))
    component_address = Column(String(2048))
    description = Column(String)
    blueprint_slug: Mapped[str] = mapped_column(ForeignKey("blueprint.slug"))
    token_address = Column(String)
    owner_token_address = Column(String)
    image = Column(String)
    owner_address = Column(String, ForeignKey('users.public_address'))


class Participants(Base):
    __tablename__ = 'participants'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    community_id = Column(UUID(as_uuid=True), ForeignKey('community.id'))
    user_addr = Column(String, ForeignKey('users.public_address'))


# Create an engine
engine = create_engine(
    'postgresql://pandao_backend_user:OGGePTvQNfp97DMRJfhp0c52WbBCZFBL@dpg-cp8s5etds78s73c8pqhg-a.oregon-postgres.render.com/pandao_backend')
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
dbsession = Session()
