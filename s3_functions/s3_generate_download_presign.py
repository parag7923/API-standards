import requests

def generate_presigned_download_url(s3_key):
    """
    Generates a presigned download URL for an S3 object using a custom API.

    :param s3_key: The S3 key for the object.
    :return: The presigned download URL.
    """
    base_url = 'https://mkpl-user.dev.devsaitech.com/api/v1/ai-resource/presigned-download'
    
    headers = {
        'accept': 'application/json',
        'x-publisher-key': 'UK24XC7qjGpeUqPo69tL6fxyt4cSXvmwZ7sYFu4nH7mKjXZyHeyHXTMVtup48hSf',
    }
    
    params = {
        's3Key': s3_key,
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    # print(response.json())
    response_data = response.json()
    presigned_url = response_data.get('data', {}).get('url')
    # print(presigned_url)
    return presigned_url

# Example usage
s3_key = "0029781988958338526/1d8b3fb7-951d-4916-a6f1-bdc77ebc9269-apple.png"
download_url = generate_presigned_download_url(s3_key)
if download_url:
    print(f"Download URL: {download_url}")
