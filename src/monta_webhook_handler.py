import json
import logging
import boto3
import uuid
from decimal import Decimal

# Initialize DynamoDB with explicit region for consistency
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3') [cite: 2026-01-20, 2026-01-25]
table = dynamodb.Table('monta_webhook_events')

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal types to float for JSON responses."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    try:
        # Load body and ensure it's a valid dictionary
        raw_payload = event.get('body', '{}')
        body_dict = json.loads(raw_payload)
        
        # Robust categorization logic [cite: 2026-01-25]
        entries = body_dict.get("entries")
        
        if body_dict.get("object") == "charge-point":
            event_category = "CHARGE_POINT"
        # Validate that 'entries' is a non-empty list [cite: 2026-01-25]
        elif isinstance(entries, list) and len(entries) > 0:
            first_entry = entries[0]
            # Ensure the first entry is a dictionary [cite: 2026-01-25]
            if isinstance(first_entry, dict):
                event_category = first_entry.get("entityType", "UNKNOWN_ENTRY_TYPE")
            else:
                event_category = "INVALID_ENTRY_FORMAT"
        else:
            event_category = "GENERIC_WEBHOOK"
        
        logger.info(f"Processing event. Category: {event_category}")
        
        # Prepare item for DynamoDB
        db_item = {
            'webhook_id': str(uuid.uuid4()),
            'event_category': event_category,
            'payload': body_dict
        }
        
        # Store in DynamoDB
        table.put_item(Item=db_item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Webhook received and stored',
                'id': db_item['webhook_id'],
                'category': event_category
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'processing_failed', 'msg': str(e)})
        }