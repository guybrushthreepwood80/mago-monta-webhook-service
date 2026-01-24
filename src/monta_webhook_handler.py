import json
import logging
import boto3
import uuid
from decimal import Decimal

# 1. DynamoDB initialisieren
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('monta_webhook_events')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Hilfsklasse, um Decimal-Werte wieder in JSON für die Response umzuwandeln
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    raw_payload = event.get('body', '{}')

    try:
        # WICHTIG: parse_float=Decimal löst das Problem mit den Float-Werten in DynamoDB
        body_dict = json.loads(raw_payload, parse_float=Decimal)
        
        # --- Dynamische Kategorisierung ---
        if body_dict.get("identifikator") == "weather":
            event_category = "WEATHER_DATA"
        elif "entries" in body_dict and len(body_dict["entries"]) > 0:
            first_entry = body_dict["entries"][0]
            # Nimmt den entityType (z.B. charge) und macht MONTA_CHARGE daraus
            etype = first_entry.get('entityType', 'generic')
            event_category = f"MONTA_{etype.upper()}"
        else:
            event_category = "UNKNOWN_WEBHOOK"
        # ----------------------------------

        # Logging mit dem Custom Encoder
        log_entry = {
            "type": "WEBHOOK_DATA",
            "category": event_category,
            "content": body_dict
        }
        print(json.dumps(log_entry, cls=DecimalEncoder)) 

        # In DynamoDB speichern
        webhook_id = str(uuid.uuid4())
        table.put_item(
            Item={
                'id': webhook_id,
                'category': event_category, # Deine neue Sortier-Spalte
                'payload': body_dict,
                'request_id': context.aws_request_id
            }
        )

        return {
            'statusCode': 200, 
            'body': json.dumps({
                'status': 'received_and_stored',
                'id': webhook_id,
                'category': event_category
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
            'body': json.dumps({'error': 'processing_failed', 'msg': str(e)})
        }