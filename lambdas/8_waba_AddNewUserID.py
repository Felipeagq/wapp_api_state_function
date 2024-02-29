import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

#waba_AddNewUserID
def lambda_handler(event, context):
    """
    Crea el usuario nuevo en dynamodb waba_users
    """
    table_name = "waba_users"
    data = event.get('msg', {})
    logger.info("waba_data: %s", data)
    wa_id = data.get('wa_id')
    phone_id = data.get('phone_id')

    if not all([wa_id, phone_id]):
        error_message = "Información faltante en el evento: wa_id o phone_id no proporcionados."
        logger.error(error_message)
        return {"statusCode": 400, "body": error_message}

    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(Item=data)
        
        success_message = "Usuario añadido exitosamente."
        logger.info(success_message)
        
        return {
            "AddNewUser": success_message
        }
    except Exception as e:
        error_message = f"Error al añadir usuario a DynamoDB: {e}"
        logger.error(error_message)
        return {"statusCode": 500, "body": error_message}


# sin env
# sin layer