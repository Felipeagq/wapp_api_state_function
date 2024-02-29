import json
import logging
import static


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Extrae los datos necesarios para procesar el mensaje y los estructura para
    que puedan ser accesibles por los siguentes lambdas.
    """
    try:
        if not static.is_message(event):
            logger.error("No es un mensaje válido.")
            return {"statusCode": 400, "body": "Mensaje no válido."}
        
        extracted_data = {
            "waba_id": static.get_waba_id(event),
            "phone_id": static.get_phone_number_id(event),
            "phone_number": static.get_from_number(event),
            "timestamp": static.get_timestamp(event),
            "message_id": static.get_message_id(event),
            "type": static.get_message_type(event),
            "message": static.get_message(event),
            "wa_id": static.get_to_number(event),
            "profile": static.get_profile(event)
        }

        logger.info(f"Datos extraídos: {extracted_data}")
        return {
            "data": extracted_data
        }

    except Exception as e:
        logger.error(f"Error al procesar el evento: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

# sin env
# sin layer