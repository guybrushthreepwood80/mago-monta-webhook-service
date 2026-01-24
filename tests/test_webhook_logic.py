import json
from unittest.mock import patch, MagicMock
from monta_webhook_handler import lambda_handler

@patch('monta_webhook_handler.table')
def test_lambda_handler_categorization(mock_table):
    # Simulate a Monta webhook payload
    payload = {
        "object": "transaction",
        "entries": [{"entityType": "MONTA_CHARGE", "id": 123}]
    }
    event = {'body': json.dumps(payload)}
    
    # Call the actual handler
    response = lambda_handler(event, None)
    body = json.loads(response['body'])
    
    # Assertions
    assert response['statusCode'] == 200
    assert body['category'] == "MONTA_CHARGE"
    assert mock_table.put_item.called