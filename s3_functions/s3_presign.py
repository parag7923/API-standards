import requests

def generate_presign(s3_key):
    url = 'https://mkpl-user.dev.devsaitech.com/api/v1/ai-resource/presigned-upload'
    
    headers = {
        'accept': 'application/json',
        'x-publisher-key': 'UK24XC7qjGpeUqPo69tL6fxyt4cSXvmwZ7sYFu4nH7mKjXZyHeyHXTMVtup48hSf',
        'Content-Type': 'application/json'
    }
    
    data = {
        "s3Key": s3_key
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the response was successful (e.g., status code 201)
        if response.status_code == 201:
            response_data = response.json()
            
            # Extract the presignedUrl and key
            presigned_url = response_data['data']['presignedUrl']
            key = response_data['data']['key']
            
            # Create a dictionary with the extracted data
            result = {'presignedUrl': presigned_url, 'key': key}
            print(result)
            return result
        else:
            print(f"Request failed. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
generate_presign('apple.png')
