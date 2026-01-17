import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # 1. Body holen
    raw_payload = event.get('body', '{}')

    try:
        # 2. In Dictionary umwandeln
        body_dict = json.loads(raw_payload)
        
        # 3. Strukturiert loggen (DAS IST DER ENTSCHEIDENDE TEIL)
        # Wir packen alles in ein Dictionary und dumpen es als JSON
        log_entry = {
            "type": "WEBHOOK_DATA",
            "content": body_dict
        }
        print(json.dumps(log_entry)) 

        return {
            'statusCode': 200, 
            'body': json.dumps({'status': 'received'})
        }

    except Exception as e:
        # Fehler ebenfalls strukturiert loggen
        error_log = {
            "type": "INVALID_JSON",
            "error": str(e),
            "raw": raw_payload
        }
        print(json.dumps(error_log))
        
        return {
            'statusCode': 400, 
            'body': json.dumps({'error': 'invalid_json_format'})
        }