import uuid

from fastapi import FastAPI
from starlette import status
from .logic import health as health_handler
from .logic.auth.users import user_login_req, user_sign_up, check_user_exist, get_user_detail
from .logic.blueprint import get_blueprints, add_blueprint as add_blueprint_logic, get_blueprint_detail
from .forms import *
from .logic.blueprint.blueprint import get_blueprint_deploymanifest
from .logic.community import get_community
from .logic.community.community import create_community, get_user_community
from .utils.presignurl import get_pre_sign_url

#

def load_server(app):
    # defines routes

    @app.get('/')
    def health_check():
        return health_handler()

    @app.get('/get-resign-url/{random_id}')
    def get_pre_sign_url_route(random_id: str):
        return get_pre_sign_url(random_id)


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

    @app.get('/community', summary="get communities of the platform ", description="get communities of platform")
    def get_community_route():
        return get_community()

    @app.get('/community/{user_addr}', summary="get communities of the platform ",
             description="get communities of platform")
    def get_community_user_route(user_addr: str):
        return get_user_community(user_addr)

    # @app.post('/community', summary="create a community on platform ", description="create community on platform")
    # def post_community_route(req: CommunityCreate):
    #     create_community(req)
