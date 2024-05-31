import logging
import uuid
from select import select

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.api.forms.community import CreateCommunityForm, CommunityComment
from models import dbsession as conn, BluePrint, Community as Com, User, CommunityParticipant, UserMetaData, \
    Participants, CommunityComments
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError

# define models
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommunityCreate:
    pass


def get_community():
    communities = conn.query(Com).options(joinedload(Com.owner)).all()
    return communities


def get_user_community(user_addr: str):
    communities = conn.query(Com).options(joinedload(Com.owner)).filter(Com.owner == user_addr).all()
    return communities


def get_single_community(community_id: uuid.UUID):
    communities = conn.query(Com).options(joinedload(Com.owner)).filter(Com.id == community_id).first()
    return communities


def user_participate_in_community(user_addr: str, community_id: uuid.UUID):
    try:
        # create new user participant
        participant = CommunityParticipant(
            participant=user_addr,
            community_id=community_id,

        )
        conn.add(participant)
        conn.commit()

    except IntegrityError as e:
        conn.rollback()
        logger.error(f"Integrity error occurred: {e}")
        raise HTTPException(status_code=400,
                            detail="Integrity error: possibly duplicate entry or foreign key constraint.")

    except SQLAlchemyError as e:
        conn.rollback()
        logger.error(f"SQLAlchemy error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        conn.rollback()
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_community_participants(community_id: UUID):
    result = (
        conn.query(User.public_address, User.name, UserMetaData.image_url)
        .join(UserMetaData, User.public_address == UserMetaData.user_address)
        .join(CommunityParticipant, CommunityParticipant.participant == User.public_address)
        .filter(CommunityParticipant.community_id == community_id)
        .all()
    )

    res = []
    for data in result:
        pa, un, dp = data
        res.append(
            {
                "participant": pa,
                "name": un,
                "image_url": dp,
            }
        )

    return res


def check_user_community_status(user_addr: str, community_id: uuid.UUID):
    try:
        user_data = conn.query(CommunityParticipant).filter(CommunityParticipant.community_id == community_id,
                                                            CommunityParticipant.participant == user_addr).first()
        if user_data is None:
            return {
                "user_participated": False
            }
        else:
            return {
                "user_participated": True
            }
    except IntegrityError as e:
        conn.rollback()
        logger.error(f"Integrity error occurred: {e}")
        raise HTTPException(status_code=400,
                            detail="Integrity error: possibly duplicate entry or foreign key constraint.")

    except SQLAlchemyError as e:
        conn.rollback()
        logger.error(f"SQLAlchemy error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        conn.rollback()
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_community_comments(c_id: uuid.UUID):
    # Join the tables
    results = conn.query(CommunityComments.comment, User.name, UserMetaData.image_url,User.public_address).join(User,
                                                                                            CommunityComments.commented_by == User.public_address).join(
        UserMetaData, User.public_address == UserMetaData.user_address).filter(
        CommunityComments.community_id == c_id).all()

    # Format the response
    comments = [
        {
            "comment": row.comment,
            "user_name": row.name,
            "user_image": row.image_url,
            "user_address":row.public_address,
        }
        for row in results
    ]

    return comments


def add_community_comment(req: CommunityComment):
    try:
        c_id = req.community_id
        u_adr = req.user_addr
        c = req.comment

        new_comment = CommunityComments(
            community_id=c_id,
            commented_by=u_adr,
            comment=c
        )
        conn.add(new_comment)
        conn.commit()

    except IntegrityError as e:
        conn.rollback()
        logger.error(f"Integrity error occurred: {e}")
        raise HTTPException(status_code=400,
                            detail="Integrity error: possibly duplicate entry or foreign key constraint.")

    except SQLAlchemyError as e:
        conn.rollback()
        logger.error(f"SQLAlchemy error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        conn.rollback()
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# error handle
def create_community(community: CreateCommunityForm):
    db_community = Com(
        name=community.name,
        component_address=community.component_address,
        description=community.description,
        owner_address=community.owner_address
    )
    conn.add(db_community)
    conn.commit()
    conn.refresh(db_community)
    return db_community
