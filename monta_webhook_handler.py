import json
import logging

# Logging Config
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Raw Payload Logging (Observability)
    raw_payload = event.get('body', '{}')
    logger.info(f"RAW_PAYLOAD: {raw_payload}")

    try:
        # JSON Parsing (Deserialization)
        data = json.loads(raw_payload)
        
        # Attribute Extraction (Logic)
        cp_id = data.get('chargePointId', 'unknown')
        logger.info(f"CHARGE_POINT_ID: {cp_id}")
        
        # API Response (Success)
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'processed'})
        }
        
    except Exception as e:
        # Error Handling (Exception Management)
        logger.error(f"PARSE_ERROR: {str(e)}")
        return {
            'statusCode': 400, 
            'body': json.dumps({'error': 'invalid_json'})
        }