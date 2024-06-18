from app.api.forms.transaction_manifest import DeployTokenWeightedDao


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
            f'Address("package_tdx_2_1p57awgxeyqqmflhy7zvzu890294hnevtwr9ufqd9uqwxymf9xtjtee")\n'
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
