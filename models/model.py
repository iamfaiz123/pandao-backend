from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, DECIMAL
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
    community: Mapped[list["Community"]] = relationship("Community", back_populates="owner")


class UserMetaData(Base):
    __tablename__ = 'user_meta_data'
    user_address: Mapped[str] = Column(String, ForeignKey('users.public_address'), primary_key=True)
    about: Mapped[str] = Column(String)
    image_url: Mapped[str] = Column(String)
    website_url: Mapped[str] = Column(String)
    x_url: Mapped[str] = Column(String)
    linkedin: Mapped[str] = Column(String)
    tiktok: Mapped[str] = Column(String)
    user: Mapped["User"] = relationship("User", back_populates="usermetadata")


class UserActivity(Base):
    __tablename__ = 'user_activity'
    transaction_id: Mapped[str] = Column(String, primary_key=True)
    # this contains a basic info about a user transaction in the DAO
    transaction_info: Mapped[str] = Column(String)
    user_address: Mapped[str] = Column(String, ForeignKey('users.public_address'))


class Community(Base):
    __tablename__ = 'community'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    component_address: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    owner_address: Mapped[str] = mapped_column(String, ForeignKey("users.public_address"))
    owner: Mapped["User"] = relationship("User", back_populates="community")
    community_comment: Mapped[list['CommunityComments']] = relationship("CommunityComments", back_populates="community")


class CommunityComments(Base):
    __tablename__ = 'community_comments'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    community_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("community.id"))
    commented_by: Mapped[str] = mapped_column(String, ForeignKey("users.public_address"))
    # commented_at: Mapped[DateTime] = Column(DateTime, default=func.now())
    comment: Mapped[str] = mapped_column(String)
    community: Mapped["Community"] = relationship("Community", back_populates="community_comment")


class CommunityParticipant(Base):
    user_addr = None
    __tablename__ = 'community_participant'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    participant: Mapped[str] = Column(String, ForeignKey("users.public_address"))
    community_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("community.id"))


class Participants(Base):
    __tablename__ = 'participants'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    community_id = Column(UUID(as_uuid=True), ForeignKey('community.id'))
    user_addr = Column(String, ForeignKey('users.public_address'))


class BluePrint(Base):
    __tablename__ = 'blueprint'
    slug: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(DECIMAL)
    package_addr = Column(String, nullable=False)

    # define relationships
    terms: Mapped[list["BluePrintTerms"]] = relationship("BluePrintTerms", back_populates="blueprint")
    methods: Mapped[list["BluePrintMethod"]] = relationship("BluePrintMethod", back_populates="blueprint")
    deploy_mainfest: Mapped["DeployManifest"] = relationship("DeployManifest", back_populates="blueprint")


class DeployManifest(Base):
    __tablename__ = 'deploymanifest'
    manifest: Mapped[str] = Column(String, primary_key=True)
    blueprint_slug: Mapped[str] = Column(String, ForeignKey('blueprint.slug'), unique=True)
    blueprint: Mapped['BluePrint'] = relationship("BluePrint", back_populates="deploy_mainfest")
    deploymanifestargs: Mapped[list['DeployManifestArgs']] = relationship("DeployManifestArgs",
                                                                          back_populates="manifest")


class DeployManifestArgs(Base):
    __tablename__ = 'deploymanifestargs'
    key: Mapped[str] = Column(String, primary_key=True)
    type: Mapped[str] = Column(String)
    blueprint_slug: Mapped[str] = Column(String, ForeignKey('deploymanifest.blueprint_slug'))
    manifest: Mapped['DeployManifest'] = relationship("DeployManifest", back_populates="deploymanifestargs")


class BluePrintTerms(Base):
    __tablename__ = 'blueprint_terms'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    term: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    blueprint_slug: Mapped[str] = mapped_column(ForeignKey("blueprint.slug"))
    blueprint: Mapped["BluePrint"] = relationship("BluePrint", back_populates="terms")


class BluePrintMethod(Base):
    __tablename__ = 'blueprint_methods'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blueprint_slug: Mapped[str] = mapped_column(ForeignKey("blueprint.slug"))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    blueprint: Mapped["BluePrint"] = relationship("BluePrint", back_populates="methods")


# Create an engine
engine = create_engine(
    'postgresql://pandao_backend_user:OGGePTvQNfp97DMRJfhp0c52WbBCZFBL@dpg-cp8s5etds78s73c8pqhg-a.oregon-postgres.render.com/pandao_backend')
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
dbsession = Session()
