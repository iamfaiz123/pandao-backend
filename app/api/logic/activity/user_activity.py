import uuid

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.api.forms.blueprint import DeployCommunity
# from app.api.forms.blueprint import DeployCommunity
from models import dbsession as conn, BluePrint, Community as Com, User, Participants, UserActivity, UserMetaData
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError


def get_user_activity():
    try:
        results = conn.query(
            UserActivity.transaction_id,
            #UserActivity.nr,
            UserActivity.user_address,
            User.name,
            UserMetaData.image_url
        ).join(
            User, UserActivity.user_address == User.public_address
        ).join(
            UserMetaData, User.public_address == UserMetaData.user_address
        ).all()
        return results
    except SQLAlchemyError as e:
        # Log the error e
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
