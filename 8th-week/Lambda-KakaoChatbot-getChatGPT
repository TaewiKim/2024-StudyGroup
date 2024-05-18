import json
import boto3
import urllib.request
import datetime
from send_response import send_response
import os

# AWS 설정 구성
region = 'ap-northeast-2'
session = boto3.Session(region_name=region)

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Read content from the "GPT_system_role.txt" file
with open("SystemMessage.txt", "r", encoding="utf-8") as file:
    system_role = file.read()

# dynamodb table
dynamodb = boto3.resource("dynamodb")
table_name = 'DynamoDB-KakaoChatbot-MiroMentis-userUtterance'
table = dynamodb.Table(table_name)

# 서울 시간대 오프셋
seoul_offset = datetime.timezone(datetime.timedelta(hours=9))

def lambda_handler(event, context):
    # Extract the SQS message body
    sqs_record = event['Records'][0]
    message_body = sqs_record['body']
    
    # Parse the JSON string into a dictionary
    message_body_dict = json.loads(message_body)
    
    # Extract user_utterance and callbackUrl from the message
    user_id = message_body_dict['userRequest']['user']['id']
    user_utterance = message_body_dict['userRequest']['utterance']
    callback_url = message_body_dict['userRequest']['callbackUrl']

    # 현재 시간을 서울 시간대로 설정
    now = datetime.datetime.now(tz=seoul_offset)

    # datetime 형식의 값을 문자열로 변환
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # 대화 불러오기
        response = table.query(
            KeyConditionExpression='UserID = :user_id',
            ExpressionAttributeValues={
                ':user_id': user_id
            },
            ScanIndexForward=False,
            Limit=5
        )
        
        chat_history = [item['message'] for item in response['Items']]
        chat_history.reverse()
        
        table.put_item( 
            Item = {
                'UserID': user_id,
                'Timestamp': timestamp,
                'message': {"content": user_utterance, "role": "user"}
            }
        )
        
        messages = [{'role': "system", "content": system_role}] + chat_history + [{'role': "user", "content": user_utterance}]
        
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }
        
        data = {
            "model": "gpt-3.5-turbo-1106",
            "max_tokens" : 500,
            "messages": messages
        }
        
        encoded_data = json.dumps(data).encode('utf-8')
        request = urllib.request.Request(url, data=encoded_data, headers=headers, method='POST')
        
        with urllib.request.urlopen(request) as response:
            response_body = json.loads(response.read().decode('utf-8'))
        
        chat_gpt_response = response_body['choices'][0]['message']['content']
                
        send_response(callback_url, chat_gpt_response)
        
        now = datetime.datetime.now(tz=seoul_offset)
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        
        table.put_item( 
            Item = {
                'UserID': user_id,
                'Timestamp': timestamp,
                'message': {"content": chat_gpt_response, "role": "assistant"}
            }
        )
        
        return {
            'statusCode': 200,
            'body': 'Response sent to KakaoTalk'
        }
        
    except Exception as error:
        print(f'getChatGPT Lambda Error: {error}')
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }
