import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    entry = event.get("entry", [{}])[0]
    changes = entry.get("changes", [{}])[0]
    value = changes.get("value", {})
    data = None

    phone_number = value["metadata"]["display_phone_number"]
    
    if not all([changes, value]):
        logger.error("status no proporcionados.")
        return {"statusCode": 400, "body": "status no proporcionado."}

    if "statuses" in value:
        status = value["statuses"][0]["status"]
        data = value["statuses"]
        logger.info("Message Confimation : %s", data)
        return {
            "statusCode": 200,
            "body": f"Message Confimation {status}", 
            "phone_number": phone_number,
            "data": data,
        }
    else:
        logger.error("status no proporcionados.")
        return {"statusCode": 400, "body": "status no proporcionado."}
    
# sin capas y sin env