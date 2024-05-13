import boto3
import datetime

# AWS 설정 구성
region = 'ap-northeast-2'
session = boto3.Session(region_name=region)

# dynamodb table
dynamodb = boto3.resource("dynamodb")
table_name = 'Your table name'
table = dynamodb.Table(table_name)

# 서울 시간대 오프셋
seoul_offset = datetime.timezone(datetime.timedelta(hours=9))

# 대화 불러오기
# Get the 5 most recent chat messages
        response = table.query(
            KeyConditionExpression='UserID = :user_id',
            ExpressionAttributeValues={
                ':user_id': user_id
            },
            ScanIndexForward=False,
            Limit=5
        )

# json 포멧 변경하기
        chat_history = []
        for item in response['Items']:
            chat_history.append(item['message'])
            
        # 대화 순서대로 정렬하기기
        chat_history = list(reversed(chat_history))

# 프롬프트 구성하기기
        messages = chat_history.copy()  # chat_history를 복사하여 messages 리스트에 추가
        
        messages.insert(0, {
            "role": "system",
            "content": system_role 
        })
        
        messages.append({
            "role": "user",
            "content": user_utterance
        })

# ChatGPT의 응답 저장하기
        table.put_item( 
                Item = {
                'UserID': user_id,
                'UserKey': plusfriend_user_key,
                'Timestamp': timestamp,
                'message': {"content": chat_gpt_response, "role": "assistant"}
            }
        )



# 새로운 대화 저장하기
        table.put_item( 
                Item = {
                'UserID': user_id,
                'UserKey': plusfriend_user_key,
                'Timestamp': timestamp,
                'message': {"content": user_utterance, "role": "user"}
            }
        )
