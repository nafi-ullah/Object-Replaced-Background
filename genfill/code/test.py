import os
import requests
from io import BytesIO
from urllib.parse import urlencode

# Set our creds based on environment variables.
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_access_token(id, secret):
    params = {
        'grant_type': 'client_credentials',
        'client_id': id,
        'client_secret': secret,
        'scope': 'openid,AdobeID,firefly_enterprise,firefly_api,ff_apis'
    }
    response = requests.post('https://ims-na1-stg1.adobelogin.com/ims/token/v3', data=urlencode(params))
    data = response.json()
    return data['access_token']

def upload_image(file_path, file_type, id, token):
    with open(file_path, 'rb') as file:
        file_size = os.path.getsize(file_path)
        headers = {
            'Authorization': f'Bearer {token}',
            'X-API-Key': id,
            'Content-Type': file_type,
            'Content-Length': str(file_size)
        }
        response = requests.post(
            'https://firefly-api-enterprise-stage.adobe.io/v2/storage/image',
            headers=headers,
            data=file
        )
    return response.json()

def download_file(url, file_path):
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def gen_fill(mask_id, source_id, width, height, prompt, id, token):
    body = {
        'numVariations': 1,
        'size': {
            'width': width,
            'height': height
        },
        'prompt': prompt,
        'image': {
            'mask': {
                'uploadId': mask_id
            },
            'source': {
                'uploadId': source_id
            }
        }
    }
    headers = {
        'X-Api-Key': id,
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(
        'https://firefly-api-enterprise-stage.adobe.io/v3/images/fill',
        headers=headers,
        json=body
    )
    return response.json()

# Main Execution
token = get_access_token(CLIENT_ID, CLIENT_SECRET)

upload = upload_image('./dog1_masked_inverted.png', 'image/png', CLIENT_ID, token)
masked_image = upload['images'][0]['id']

upload = upload_image('./dog1.png', 'image/png', CLIENT_ID, token)
source_image = upload['images'][0]['id']

result = gen_fill(masked_image, source_image, 2048, 2048, "a garden beside road", CLIENT_ID, token)
file_name = './output/basic_getfill.jpg'
download_file(result['outputs'][0]['image']['url'], file_name)
