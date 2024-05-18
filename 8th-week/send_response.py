import json
import urllib.request

def send_response(callback_url, message):
    # Create a payload for the KakaoTalk message
    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": message
                    }
                }
            ]
        }
    }
    
    # Serialize the payload to a JSON string
    payload_json = json.dumps(payload, ensure_ascii=False)
    
    # Prepare the request with proper headers
    req = urllib.request.Request(callback_url, data=payload_json.encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    
    # Send the payload to the KakaoTalk API with UTF-8 encoding
    try:
        with urllib.request.urlopen(req) as response:
            # Check the response status code
            if response.status != 200:
                response_body = response.read().decode('utf-8')
                raise Exception('Failed to send response to KakaoTalk: ' + response_body)
    except urllib.error.HTTPError as e:
        # Handle specific HTTP errors
        error_message = e.read().decode()
        print(f'HTTP error occurred: {e.code} - {error_message}')
    except urllib.error.URLError as e:
        # Handle URL errors
        print(f'URL error occurred: {e.reason}')
    except Exception as e:
        # General exception handling
        print(f'An error occurred: {str(e)}')
