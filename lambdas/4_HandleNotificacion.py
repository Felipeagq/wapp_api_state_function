import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    entry = event.get("entry", [{}])[0]
    changes = entry.get("changes", [{}])[0]
    value = changes.get("value", {})

    
    if not all([changes, value]):
        logger.info("configurando endpoint")
        return {"statusCode": 200, "body": "configurando endpoint"}

    if "alert_state" in value:
        logger.warning("Alert Notification : %s", value)
        return {"statusCode": 200, "body": "Alert Notification", "data": value}
    else:
        logger.error("alert_state no proporcionados.")
        return {"statusCode": 400, "body": "alert_state no proporcionado."}

# sin env
# sin layer