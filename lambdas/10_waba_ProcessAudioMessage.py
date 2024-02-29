import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def lambda_handler(event, context):
    """Procesa mensajes de texto entrantes de WhatsApp."""
    logger.info("Se está procesando un audio: %s", response)
    
    message = event.get('message')

    if not message or not from_number:
        return {"statusCode": 400, "body": "Faltan datos en el evento."}
    
    response = "mensaje de audio procesado"
    logger.info("Mensaje enviado con éxito: %s", response)
    return {"statusCode": 200, "body": "mensaje de audio procesado"}

