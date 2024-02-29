import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    """
    Realiza la consulta en la tabla de dynamodb waba_users para verificar si
    el usuario ya tiene su numero registrado en la 
    """
    data = event.get('msg', {})
    logger.info("Data Recibida: %s", data)
    wa_id = data.get('wa_id', {})
    phone_id = data.get('phone_id')

    if not wa_id:
        logger.error("wa_id no proporcionado en el evento.")
        return {"statusCode": 400, "body": "wa_id no proporcionado."}

    table = dynamodb.Table("waba_users")

    try:
        response = table.get_item(Key={'wa_id': wa_id, 'phone_id': phone_id})
    except Exception as e:
        logger.error("Error al acceder a DynamoDB: %s", e)
        return {"statusCode": 500, "body": "Error al acceder a la base de datos."}

    user_exists = 'Item' in response

    return {
        "userExists": user_exists,
        "wa_id": wa_id,
        "phone_id": phone_id
    }


# sin env
# sin layer