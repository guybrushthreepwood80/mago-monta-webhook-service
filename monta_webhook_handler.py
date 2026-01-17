import json
import logging

# Logging Config
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # 1. Alles loggen (Observability)
    raw_payload = event.get('body', '{}')
    logger.info(f"WEBHOOK_DATA: {raw_payload}")

    try:
        # 2. Validierung (Check if it's valid JSON)
        json.loads(raw_payload)
        
        return {
            'statusCode': 200, 
            'body': json.dumps({'status': 'received'})
        }
    except Exception as e:
        # 3. Fehler-Logging
        logger.error(f"INVALID_JSON: {str(e)}")
        return {
            'statusCode': 400, 
            'body': json.dumps({'error': 'invalid_json_format'})
        }