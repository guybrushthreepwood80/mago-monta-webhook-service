"""
Author: Martin Goth
Project: Monta Webhook Integrator
Description: AWS Lambda Handler to process incoming webhooks from Monta.
"""

import json
import logging

# Logger-Setup: Wir markieren die Logs mit einem Prefix
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Ein kleiner "Stempel" in den CloudWatch Logs
    logger.info("--- [DEIN NAME]'s Webhook Processor started ---")
    
    try:
        # 1. Body checken
        if 'body' not in event or not event['body']:
            logger.warning("Empty body received.")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No data received', 'developer': '[DEIN NAME]'})
            }
        
        # 2. Daten verarbeiten
        data = json.loads(event['body'])
        
        # Beispiel: Wir loggen eine ID aus dem Webhook
        charge_point_id = data.get('chargePointId', 'unknown')
        logger.info(f"Processing Webhook for Charge Point: {charge_point_id}")
        
        # 3. Erfolgreiche Antwort
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Webhook processed by [DEIN NAME]',
                'status': 'success',
                'id': charge_point_id
            })
        }
        
    except Exception as e:
        logger.error(f"Error in [DEIN NAME]'s handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }