from http.client import HTTPException

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from models import dbsession as conn, User, UserMetaData
from ....forms import UserLogin, UserSignupForm, UserProfileUpdate
from ....utils import ApiError
import logging

logging.basicConfig(level=logging.ERROR)


def user_sign_up(signup: UserSignupForm):
    try:
        # insert user details first
        user = User(
            name=signup.username,
            public_address=signup.public_address,
        )
        # create user meta data
        usermetadata = UserMetaData(
            user_address=signup.public_address,
            about=signup.about,
            image_url=signup.display_image
        )
        user.usermetadata = usermetadata
        conn.add(user)
        conn.commit()
        return {
            "status": 201,
            "message": "user created "
        }
    except IntegrityError as e:
        conn.rollback()
        return {
            "status": 401,
            "cause": "user with same wallet address already exists"
        }
    except Exception as e:
        conn.rollback()
        logging.error("error at user signup : {}", e)
        raise HTTPException()


def user_login_req(req: UserLogin):
    try:
        conn.commit()
        response = conn.query(User).filter(User.public_address == req.public_address ).first()
        return response
    except IntegrityError:
        conn.rollback()
        return {

        }
    except Exception as e:
        conn.rollback()
        logging.error(e)
        return ApiError("Something went wrong, we're working on it", 500).as_http_response()

##
def get_user_detail(public_address: str):
    try:
        stmt = (select(User.public_address, User.name, UserMetaData.about, UserMetaData.image_url)
                .join(UserMetaData, User.public_address == UserMetaData.user_address)).where(User.public_address == public_address)
        result = conn.execute(stmt).first()
        if result is None:
            return {
                "status": 404,
                "cause": "user with these credentials does not exist"
            }
        else:
            pub_addr, name, about, img = result
            return {
                'public_address': pub_addr,
                'name': name,
                'about': about,
                'image_url': img
            }

    except Exception as e:
        conn.rollback()
        logging.error(e)
        return ApiError("Something went wrong, we're working on it", 500).as_http_response()


def check_user_exist(public_address: str):
    try:
        user_status = conn.query(User).filter(User.public_address == public_address).first()
        if user_status is not None:
            return {
                "user_address": public_address,
                "exist": True
            }
        else:
            return {
                "user_address": public_address,
                "exist": False
            }
    except Exception as e:
        logging.error("Error getting user signup status: %s", e)
        raise HTTPException()

def update_user_profile(req:UserProfileUpdate):
    try:
        user_meta_data = conn.query(UserMetaData).filter(UserMetaData.user_address == req.public_address).first()
        if user_meta_data is None:
            return {
                "status": 404,
                "cause": "user with these credentials does not exist"
            }

        if req.about is not None:
            user_meta_data.about = req.about
        if req.image_url is not None:
            user_meta_data.image_url = req.image_url
        if req.tiktok is not None:
            user_meta_data.tiktok = req.tiktok
        if req.x_url is not None:
            user_meta_data.x_url = req.x_url
        # if req.website_url is not None:
        #     user_meta_data.website_url = req.website_url
        if req.linkedin is not None:
            user_meta_data.linkedin = req.linkedin

        conn.commit()
        conn.refresh(user_meta_data)
        return user_meta_data

    except Exception as e:
        conn.rollback()
        logging.error(e)
        return ApiError("Something went wrong, we're working on it", 500).as_http_response()


