from http.client import HTTPException

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from models import dbsession as conn, User, UserMetaData
from ....forms import UserLogin, UserSignupForm
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
    # extract data from form
    wallet_addr = req.public_address
    name = req.name
    user = User(name=name, public_address=wallet_addr)
    conn.add(user)
    try:
        conn.commit()
        response = conn.query(User).all()
        return response
    except IntegrityError:
        conn.rollback()
        return {}
    except Exception as e:
        conn.rollback()
        logging.error(e)
        return ApiError("Something went wrong, we're working on it", 500).as_http_response()


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
