import json
import logging
import boto3
import uuid
from decimal import Decimal

# 1. DynamoDB initialisieren mit expliziter Region für Paris
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3') [cite: 2026-01-20, 2026-01-25]
table = dynamodb.Table('monta_webhook_events')

# Hilfsklasse, um Decimal-Werte wieder in JSON für die Response umzuwandeln
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    try:
        # Body laden und sicherstellen, dass ein Dictionary vorliegt
        raw_payload = event.get('body', '{}')
        body_dict = json.loads(raw_payload)
        
        # --- Robuste Kategorisierungs-Logik --- [cite: 2026-01-25]
        entries = body_dict.get("entries")
        
        if body_dict.get("object") == "charge-point":
            event_category = "CHARGE_POINT"
        # Validierung: Ist 'entries' eine Liste und enthält mindestens ein Element? [cite: 2026-01-25]
        elif isinstance(entries, list) and len(entries) > 0:
            first_entry = entries[0]
            # Sicherstellen, dass das Element ein Dictionary ist [cite: 2026-01-25]
            if isinstance(first_entry, dict):
                event_category = first_entry.get("entityType", "UNKNOWN_ENTRY_TYPE")
            else:
                event_category = "INVALID_ENTRY_FORMAT"
        else:
            event_category = "GENERIC_WEBHOOK"
        
        # Logging mit dem neuen Event-Typ
        logger.info(f"Processing event. Category: {event_category}")
        
        # Payload für DynamoDB vorbereiten (mit UUID und Timestamp)
        db_item = {
            'webhook_id': str(uuid.uuid4()),
            'event_category': event_category,
            'payload': body_dict
        }
        
        # In DynamoDB speichern
        table.put_item(Item=db_item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Webhook received and stored',
                'id': db_item['webhook_id'],
                'category': event_category
            })
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'processing_failed', 'msg': str(e)})
        }