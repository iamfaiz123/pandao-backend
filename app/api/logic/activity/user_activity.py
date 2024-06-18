# import uuid
#
# from sqlalchemy import or_
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import joinedload
#
# from app.api.forms.blueprint import DeployCommunity
# # from app.api.forms.blueprint import DeployCommunity
# from models import dbsession as conn, BluePrint, Community as Com, User, Participants
# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy.exc import SQLAlchemyError
# def get_user_activity(user_id):
#     try:
#         activity = conn.query(UserActivity).join()
