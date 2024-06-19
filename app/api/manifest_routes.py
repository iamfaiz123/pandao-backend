from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.forms.transaction_manifest import DeployTokenWeightedDao, BuyTokenWeightedDaoToken
from models import Community
from models import dbsession as conn


def transaction_manifest_routes(app):
    @app.post('/manifest/build/deploy_token_weighted_dao', tags=(['manifest_builder']))
    def build_token_weight_deploy_manifest(req: DeployTokenWeightedDao):
        organization_name = req.communityName
        token_supply = req.tokenSupply
        token_price = req.tokenPrice
        token_withdraw_price = req.tokenWithDrawPrice
        organization_image = req.communityImage
        organization_token_image = req.tokenImage
        user_account = req.userAddress
        manifest = command_string = (
            f'CALL_FUNCTION\n'
            f'Address("package_tdx_2_1p5vl40wrmr49mvjqzmchjjvcq5ctq5mad9he6svkymrzqm5236jsr8")\n'
            f'"TokenWeigtedDao"\n'
            f'"initiate"\n'
            f'"{organization_name}"\n'
            f'{token_supply}i32\n'
            f'0u8\n'
            f'Decimal("{token_price}")\n'
            f'Decimal("{token_withdraw_price}")\n'
            f'"{organization_image}"\n'
            f'"{organization_token_image}"\n'
            f';\n'
            f'CALL_METHOD\n'
            f'    Address("{user_account}")\n'
            f'    "deposit_batch"\n'
            f'    Expression("ENTIRE_WORKTOP")\n'
            f';'
        )
        return manifest

    @app.post('/manifest/build/buy_token/token_weighted_dao', tags=(['manifest_builder']))
    def buy_token_token_weighted_dao(req: BuyTokenWeightedDaoToken):
     try:
        community = conn.query(Community).filter(Community.id == req.community_id).first()
        account_address = req.userAddress
        XRD_take = req.tokenSupply + 3
        community_address = community.component_address
        token_take = req.tokenSupply

        transaction_string = f"""
        CALL_METHOD
            Address("{account_address}")
            "withdraw"
            Address("resource_tdx_2_1tknxxxxxxxxxradxrdxxxxxxxxx009923554798xxxxxxxxxtfd2jc")
            Decimal("{XRD_take}")
        ;

        TAKE_FROM_WORKTOP
            Address("resource_tdx_2_1tknxxxxxxxxxradxrdxxxxxxxxx009923554798xxxxxxxxxtfd2jc")
            Decimal("{XRD_take}")
            Bucket("bucket1")
        ;

        CALL_METHOD
        Address("{community_address}")
        "obtain_token"
        Bucket("bucket1")
        Decimal("{token_take}")
        ;

        CALL_METHOD
            Address("{account_address}")
            "deposit_batch"
            Expression("ENTIRE_WORKTOP")
        ;
        """
        return transaction_string

     except SQLAlchemyError as e:
        # Log the error e
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
