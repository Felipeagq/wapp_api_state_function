import json
import boto3
import os
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    """
    Consulta el dynamodb waba_users y debe obtener los datos del usuario para
    procesar correctamente con openai su respuesta.
    
    #TODO se debe estructurar la asignacion del Assistant_ID para que cuando
    el usuario haga la petición se procese su respuesta con el mismo asistente.
    
    #TODO tambien se debe implementar el chat_history en dynamodb
    """
    table_name = "waba_users"
    
    data = event.get('msg', {})
    wa_id = data.get('wa_id')
    phone_id = data.get('phone_id')
    msg_type = data.get('type')
    
    if not all([wa_id, phone_id]):
        logger.error("wa_id o phone_id no proporcionados.")
        return {"statusCode": 400, "body": "wa_id no proporcionado."}

    table = dynamodb.Table(table_name)

    try:
        # response = table.get_item(Key={'wa_id': wa_id})
        # if 'Item' not in response:
        #     logger.error("Usuario no encontrado en la base de datos.")
        #     return {"statusCode": 404, "body": "Usuario no encontrado."}

        # user_data = response['Item']

        # Realiza aquí las operaciones necesarias con user_data
        # Por ejemplo, actualizar algún registro o realizar una acción específica

        return {
            "type": msg_type,
            "wa_id": wa_id
        }
    except Exception as e:
        logger.error("Error al procesar el usuario existente: %s", e)
        return {"statusCode": 500, "body": "Error al procesar el usuario existente."}

# sin env
# sin layer
