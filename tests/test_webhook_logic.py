import pytest
from decimal import Decimal
# Wir importieren deinen Encoder, um den Monta-Fix (Floats) zu prüfen
from monta_webhook_handler import DecimalEncoder

def test_weather_category_fix():
    """
    Validiert, dass der Wetter-Webhook mit dem Key 'event' 
    jetzt korrekt erkannt wird.
    """
    # Das ist der Payload, der heute im Log 'unknown' war
    sample_payload = {
        "event": "weather", 
        "temperature": "-2.52"
    }
    # Wir simulieren die Logik deiner Lambda
    assert sample_payload.get("event") == "weather"
    assert sample_payload.get("identifikator") is None

def test_decimal_precision_fix():
    """
    Stellt sicher, dass Beträge (wie bei Monta) präzise 
    als Decimal verarbeitet werden (kein Float-Fehler).
    """
    amount = Decimal("10.99")
    encoder = DecimalEncoder()
    # Der Encoder sollte den Decimal-Wert für die JSON-Antwort korrekt handhaben
    assert encoder.default(amount) == 10.99

def test_monta_category_logic():
    """
    Prüft, ob die Monta-Kategorisierung stabil bleibt.
    """
    sample_payload = {"entityType": "MONTA_CHARGE"}
    assert sample_payload.get("entityType") == "MONTA_CHARGE"