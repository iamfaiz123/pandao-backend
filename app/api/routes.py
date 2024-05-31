import uuid

from fastapi import FastAPI
from starlette import status

from .forms.community import CreateCommunityForm, CommunityParticipant
from .logic import health as health_handler
from .logic.auth.users import user_login_req, user_sign_up, check_user_exist, get_user_detail, update_user_profile
from .logic.blueprint import get_blueprints, add_blueprint as add_blueprint_logic, get_blueprint_detail
from .forms import *
from .logic.blueprint.blueprint import get_blueprint_deploymanifest
from .logic.community import get_community
from .logic.community.community import create_community, get_user_community, user_participate_in_community, \
    get_community_participants, get_single_community, check_user_community_status
from .utils.presignsignature import generate_signature


#

def load_server(app):
    # defines routes

    @app.get('/')
    def health_check():
        return health_handler()

    @app.get("/image-upload/signature")
    def get_image_upload_signature_route():
        return generate_signature()

    # api for user to register
    @app.post('/user/signup', status_code=status.HTTP_201_CREATED)
    def user_signup_route(req: UserSignupForm):
        return user_sign_up(req)

    @app.get('/user/check-signup/{public_address}', status_code=status.HTTP_200_OK)
    def user_check_signup_route(public_address: str):
        return check_user_exist(public_address)

    @app.get('/user/details/{public_address}', status_code=status.HTTP_200_OK)
    def get_user_details_route(public_address: str):
        return get_user_detail(public_address)

    @app.post('/user/login', status_code=status.HTTP_201_CREATED)
    def register(req: UserLogin):
        return user_login_req(req)

    @app.patch('/user/update-user', status_code=status.HTTP_200_OK)
    def update_user_route(req: UserProfileUpdate):
        return update_user_profile(req)

    # define routes for blueprints
    @app.get('/blueprint', summary="Get all blueprints", description="use to get all blueprint",
             status_code=status.HTTP_201_CREATED)
    def get_blueprint_route():
        return get_blueprints()

    @app.get('/blueprint/detail/{slug}', summary="get detail about a single blueprint",
             description="get detail about a single blueprint")
    def get_blueprint_route(slug: str):
        return get_blueprint_detail(slug)

    @app.get('/blueprint/manifest/{slug}', summary="get blueprint manifest",
             description="get manigest and args of a blueprint")
    def get_blueprint_manifest_route(slug: str):
        return get_blueprint_deploymanifest(slug)

    @app.post('/blueprint', summary="add a blueprint ", description="add blue print by admin")
    def add_blueprint_route(req: BlurPrintForm):
        add_blueprint_logic(req)

    @app.post('/community', summary='create a new community')
    def create_community_route(req: CreateCommunityForm):
        return create_community(req)

    @app.get('/community', summary="get communities of the platform ", description="get communities of platform")
    def get_community_route():
        return get_community()

    @app.get('/community/detail/{c_id}', summary="get community detail")
    def get_community_detail_route(c_id: uuid.UUID):
        return get_single_community(c_id)

    @app.get('/community/check/user_status', summary="check if user is participant of community")
    def check_user_community_status_route(user_addr: str, community_id: uuid.UUID):
        return check_user_community_status(user_addr, community_id)

    # @app.get('/community/{user_addr}', summary="get communities of the platform ",
    #          description="get communities of platform")
    # def get_community_user_route(user_addr: str):
    #     return get_user_community(user_addr)

    @app.post('/community/participant', summary="user join a community")
    def join_community(req: CommunityParticipant):
        return user_participate_in_community(req.participant_address, req.community_id)

    @app.get('/community/participant/{c_id}', summary="user join a community")
    def get_community_participant_route(c_id: uuid.UUID):
        return get_community_participants(c_id)
