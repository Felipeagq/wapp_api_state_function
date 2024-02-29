import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Este modulo se encarga de recibir el json de WhatsApp API y lo procesa 
    para extraer el tipo de mensaje entre: Mensaje del Usuario, Notificación,
    Mensaje de Status de WhatsApp
    """
    try:
        entries = event.get("entry", [])
        if not entries:
            encript = event.get("encrypted_flow_data", [])
            if encript:
                return {
                    "type": "encrypted_flow_data",
                    "data": event
                }
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                if "messages" in value:
                    messages = value["messages"]
                    for message in messages:
                        if message.get("type") == "interactive":
                            interactive = message.get("interactive", {})
                            if interactive.get("type") == "nfm_reply":
                                nfm_reply = interactive.get("nfm_reply", {})
                                if nfm_reply.get("name") == "flow":
                                    return {
                                        "type": "flow_completion",
                                        "data": nfm_reply.get("response_json")
                                    }
                    return {
                        "type": "message"
                    }
                elif "event" in value:
                    return {
                        "type": "notification",
                        "data": value
                    }
                elif "statuses" in value:
                    return {
                        "type": value["statuses"][0]["status"],
                        "data": value["statuses"]
                    }
                else:
                    return {
                        "type": "Unsupported",
                        "data": value
                    }

                #return {"type": "Unsupported"}

    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        return {"statusCode": 500, "body": "Internal Server Error"}



# env
# WP_TOKEN 

# layer 
# arn:aws:lambda:us-east-2:315068324448:layer:openai_pywa:1