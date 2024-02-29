import json
import logging
import base64
from pywa import RSA, AES

logger = logging.getLogger()
logger.setLevel(logging.INFO)
YOUR_RSA_PRIVATE_KEY = "Pendiente"

def decrypt_aes_key(encrypted_key, private_key):
    rsa = RSA(private_key=private_key)
    return rsa.decrypt(base64.b64decode(encrypted_key))

def decrypt_payload(encrypted_data, aes_key, iv):
    aes = AES(key=aes_key, iv=iv, mode='GCM', tag=encrypted_data[-16:])
    return aes.decrypt(encrypted_data[:-16])

def lambda_handler(event, context):
    try:
        encrypted_data = base64.b64decode(event['encrypted_flow_data'])
        encrypted_aes_key = event['encrypted_aes_key']
        iv = base64.b64decode(event['initial_vector'])

        aes_key = decrypt_aes_key(encrypted_aes_key, YOUR_RSA_PRIVATE_KEY)
        decrypted_payload = decrypt_payload(encrypted_data, aes_key, iv)

        return {
            "statusCode": 200,
            "body": {
                "message": "Procesado con éxito",
                "decrypted_payload": decrypted_payload.decode("utf-8")
            }
        }
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        return {"statusCode": 500, "body": "Internal Server Error"}

# layer
# arn:aws:lambda:us-east-2:315068324448:layer:openai_pywa:1
