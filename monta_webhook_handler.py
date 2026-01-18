import json
import logging
import boto3
import uuid

# 1. DynamoDB initialisieren (außerhalb des Handlers)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('monta_webhook_events')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    raw_payload = event.get('body', '{}')

    try:
        body_dict = json.loads(raw_payload)
        
        # Dein strukturiertes Logging behalten wir bei
        log_entry = {
            "type": "WEBHOOK_DATA",
            "content": body_dict
        }
        print(json.dumps(log_entry)) 

        # 2. NEU: In DynamoDB speichern
        webhook_id = str(uuid.uuid4())
        table.put_item(
            Item={
                'id': webhook_id,
                'payload': body_dict,
                'request_id': context.aws_request_id
            }
        )

        return {
            'statusCode': 200, 
            'body': json.dumps({
                'status': 'received_and_stored',
                'id': webhook_id
            })
        }

    except Exception as e:
        error_log = {
            "type": "ERROR",
            "error": str(e),
            "raw": raw_payload
        }
        print(json.dumps(error_log))
        
        return {
            'statusCode': 400, 
            'body': json.dumps({'error': 'processing_failed'})
        }