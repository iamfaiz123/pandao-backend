import requests


def token_bucket_deploy_event_listener(tx_id: str):
    print('this called ')
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
        # Parse the response JSON data
        response_data = response.json()
        # Print the response JSON data

        # Store the response data in a dictionary
        response_data = response_data
        tx_events = response_data['transaction']['receipt']['events']
        # print(tx_events)
        for event in tx_events:
            if event['name'] == 'DaoDeployment':
                for field in event['data']['fields']:
                    resources[field['field_name']] = field['value']

        return resources

    else:
        print(f"Request failed with status code {response.status_code}")
