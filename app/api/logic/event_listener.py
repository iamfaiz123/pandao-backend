from http.client import HTTPException

import requests
from sqlalchemy.exc import SQLAlchemyError

from models import Community, dbsession as conn, UserActivity


## pending , add logger

def token_bucket_deploy_event_listener(tx_id: str, user_address: str):
    url = "https://babylon-stokenet-gateway.radixdlt.com/transaction/committed-details"
    data = {
        "intent_hash": tx_id,
        "receipt_events": True,
        "opt_ins": {
            "receipt_events": True
        }
    }

    # Send a POST request with the JSON data
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # create an empty dict to strore data
        resources = {}
        metadata = {}
        # Parse the response JSON data
        response_data = response.json()
        # Print the response JSON data

        # Store the response data in a dictionary

        response_data = response_data
        tx_events = response_data['transaction']['receipt']['events']
        # print(tx_events)
        for event in tx_events:
            if event['name'] == 'PandaoEvent':
                for field in event['data']['fields']:
                    print(field['field_name'])
                    if field['field_name'] == 'meta_data':
                        for m_d in field['fields']:
                            for _m_d in m_d['fields']:
                                metadata[_m_d['field_name']] = _m_d['value']


                    else:
                        resources[field['field_name']] = field.get('value') or field.get('variant_name')

        # check the event type of the tx
        try:
            if resources['event_type'] == 'DEPLOYMENT':
                # create a new community
                temp = metadata['community_name']
                community = Community(
                    name=metadata['community_name'],
                    component_address=metadata['component_address'],
                    description='some random description',
                    blueprint_slug='token-weight',
                    token_address=metadata['token_address'],
                    owner_token_address=metadata['owner_token_address'],
                    owner_address=user_address,
                    image=metadata['community_image']
                )

                # create user activity

                activity = UserActivity(
                    transaction_id=tx_id,
                    transaction_info=f'created  {temp}',
                    user_address=user_address
                )
                conn.add(community)
                conn.add(activity)
                conn.commit()
        except SQLAlchemyError as e:
            conn.rollback()
            # logger.error(f"SQLAlchemy error occurred: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return resources

    else:
        print(f"Request failed with status code {response.status_code}")
