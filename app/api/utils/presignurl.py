import requests




def get_pre_sign_url(addr:str):
    url = "https://uploadthing.com/api/uploadFiles"
    payload = {
        "files": [
            {
                "name": "",
                "size": 1,
                "type": "",
                "customId": addr
            }
        ],
        "acl": "public-read",
        "metadata": None,
        "contentDisposition": "inline"
    }
    headers = {
        "Content-Type": "application/json",
        "X-Uploadthing-Api-Key": "sk_live_ea005ab0c024f812925c5826f39afac2333fe0396c3b74c1c812cd471da5c734",
        "X-Uploadthing-Version": "6.4.0"
    }

    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    print(response)
    return {
        'url': response['data'][0]['url']
    }
