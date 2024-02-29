import os
import re
import json
import logging
from pywa import WhatsApp
from pywa.types import Message, FlowButton, Template, Button, ButtonUrl, SectionList, Section, SectionRow
from pywa.types.flows import (
    FlowStatus,
    FlowActionType,
    FlowRequest,
    FlowResponse,
    FlowCompletion,
)
from pywa.errors import WhatsAppError
from openai import OpenAI

logger = logging.getLogger()
logger.setLevel(logging.INFO)

WP_TOKEN = os.environ.get("WP_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

#{"role": "system", "content": "Responde en español con una frase creativa y divertida a incluye emojis diversos 🤖"},

def get_openai_response(text: str) -> str:
    """Obtiene una respuesta de OpenAI."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres el asistente de atención al cliente de Vianney. Vianney es una comunidad de mujeres para venta por catálogo. Siempre saluda y da la bienvenida con cariño. Responde en español e incluye emojis diversos 🤖"},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


def lambda_handler(event, context):
    """
    Procesa el mensaje de texto con openai para darle respuesta al usuario.
    
    #TODO hay que refactorizar este lambda para que cada tarea sea desagregada
    debe ser un solo lambda el que procese la respuesta con OpenAI y debe ser
    otro lambda o grupo de lambdas que le den respuesta al cliente de acuerdo
    a su petición.
    """

    data = event.get('msg', {})
    message = data.get("message", "").lower()
    to_number = data.get('wa_id')
    from_number = data.get('phone_number')
    phone_id = data.get('phone_id', {})

    if not all([message, from_number, to_number, phone_id]):
        logger.error("to_number, from_number o phone_id no proporcionados.")
        return {"statusCode": 400, "body": "to_number, from_number o phone_id no proporcionados."}
        
    wa = WhatsApp(
        phone_id=phone_id,
        token=WP_TOKEN,
        server=None,
        callback_url="https://km8nroe3fc.execute-api.us-east-2.amazonaws.com/beta/waba",
        verify_token="VERIFY",
        app_id=1042148930083483,
        app_secret="29afa077bd63316b422417bc3914cc62",
    )
    
    if re.match(r"cr[eé]dito", message) and phone_id == "111651605353893":
        response = wa.send_message(
            to=to_number,
            text='Haz click y continua tu solicitud de crédito',
            buttons=FlowButton(
                title="Quiero mi Crédito",
                flow_id="927346702296553",
                flow_token="befb09eb-977c-46ef-9162-6b307a2daaf9",
                mode=FlowStatus.PUBLISHED,
                flow_action_type=FlowActionType.NAVIGATE,
                flow_action_screen="screen_cxishi",
            )
        )
        logger.info("Flow enviado: %s a %s", response, from_number)
        return {
            "from": from_number,
            "to": to_number,
            "body": response
        }
    elif message=="cobrot" and phone_id == "164323003440635":
        response = wa.send_message(
            to=to_number,
            text='¡Hola, Helena! 😊 Espero que te encuentres muy bien. Solo quería recordarte 📅 que el pago de tu cuota está próximo a vencer en 3 días. Sería fantástico si pudieras realizar el pago de $2,453.00. Si tienes alguna duda o necesitas asistencia, estamos aquí para ayudarte. 💬 ¡Gracias!',
            buttons=FlowButton(
                title="Pagar mi Cuota",
                flow_id="297684883286855",
                flow_token="3574bfd0-194b-4d53-8574-c8dd47354719",
                mode=FlowStatus.PUBLISHED,
                flow_action_type=FlowActionType.NAVIGATE,
                flow_action_screen="START",
            )
        )
        logger.info("Flow enviado: %s a %s", response, from_number)
        return {
            "from": from_number,
            "to": to_number,
            "body": response
        }
    elif message == "producto" and phone_id == "111651605353893":
        response = wa.send_image(
            to=to_number,
            image="https://uploads-ssl.webflow.com/64d4e9c66f43bd5b11e53ff7/65b9310f434501ed7e092009_xpulse.jpg",
            caption="¡Rueda con actitud y potencia en las calles con la Hunk 160 RS!",
            footer="Powered by Neero",
            buttons=ButtonUrl(title='Compra Ahora', url='https://xpulset.heromotos.com.co/')
        )
        logger.info("Producto enviado: %s a %s", response, from_number)
        return {
            "from": from_number,
            "to": to_number,
            "body": response
        }
    elif message == "eucerin":
        response = wa.send_image(
            to=to_number,
            image="https://medipielsa.vtexassets.com/arquivos/ids/173696-1200-auto?v=637928069630300000&width=1200&height=auto&aspect=true",
            caption="Gel Limpiador Facial Dermopure Oil Control - Eucerin 200 ml",
            footer="Powered by Neero",
            buttons=ButtonUrl(title='Finaliza Ahora', url='https://www.medipiel.com.co/dermopure-oil-control-gel-limpiador--x-200ml--eucerin/p?srsltid=AfmBOopcBjkR_eT2zl-AEZeUYwH7wS9dva3kSn1Bxho_seD94HfkhrmlGCQ')
        )
        logger.info("Producto enviado: %s a %s", response, from_number)
        return {
            "from": from_number,
            "to": to_number,
            "body": response
        }
    elif message == "tostao":
        response = wa.send_image(
            to=to_number,
            image="https://vaquitaexpress.com.co/media/catalog/product/cache/e89ece728e3939ca368b457071d3c0be/7/7/7702439044787_29.jpg",
            caption="Café Tostao Gourmet Tostado Y Molido Bolsa x 454gr",
            buttons=ButtonUrl(title='Finaliza Ahora', url='https://vaquitaexpress.com.co/cafe-tostao-gourmet-tostado-y-molido-bolsa-x-454gr.html')
        )
        logger.info("Producto enviado: %s a %s", response, from_number)
        return {
            "from": from_number,
            "to": to_number,
            "body": response
        }
    elif message == "vianney":
        response = wa.send_message(
            to=to_number,
            header='Menú Vianney',
            text='Selecciona una de las siguientes opciones del menú para explorar todo lo que tenemos para ti.',
            buttons=SectionList(
                button_title='Menú',
                sections=[
                    Section(
                        title='Menú',
                        rows=[
                            SectionRow(
                                title='🔍 Consulta de productos',
                                callback_data='consulta',
                                description='Verifica disponibilidad de productos.',
                            ),
                            SectionRow(
                                title='💰 Quiero Vender Vianney',
                                callback_data='ventas',
                                description='Conviértete en Asesora Decoración.',
                            ),
                            SectionRow(
                                title='⏱️ Estatus de tu pedido',
                                callback_data='estatus',
                                description='Estado actual de tu pedido.',
                            ),
                            SectionRow(
                                title='🛒 Comprar o Hacer Pedido',
                                callback_data='comprar',
                                description='Guía para realizar compras o pedidos.',
                            ),
                            SectionRow(
                                title='📚 Nuestros Catálogos',
                                callback_data='catalogo',
                                description='Explora productos y servicios.',
                            ),
                            SectionRow(
                                title='📍 Ubícanos',
                                callback_data='ubicanos',
                                description='Encuentra tu oficina más cercana.',
                            ),
                            SectionRow(
                                title='👩 Soy ADI',
                                callback_data='soyadi',
                                description='Info y recursos para ADIs.',
                            )
                        ],
                    )
                ]
            )
        )
        logger.info("Producto enviado: %s a %s", response, from_number)
        return {
            "from": from_number,
            "to": to_number,
            "body": response
        }
    elif message == "servicio":
        response = wa.send_message(
            to=to_number,
            header='Menú Vianney',
            text='Selecciona una de las siguientes opciones del menú para explorar todo lo que tenemos para ti.',
            buttons=SectionList(
                button_title='Ventas',
                sections=[
                    Section(
                        title='Menú',
                        rows=[
                            SectionRow(
                                title='🤝 Afiliación',
                                callback_data='consulta',
                                description='Cómo unirte a nuestro programa fácilmente.',
                            ),
                            SectionRow(
                                title='💰 Beneficios',
                                callback_data='ventas',
                                description='Descubre tus ganancias y ventajas.',
                            ),
                            SectionRow(
                                title='🛒 Vigencias',
                                callback_data='estatus',
                                description='Info sobre tiempo y ventas mínimas.',
                            ),
                            SectionRow(
                                title='💸 Costo',
                                callback_data='comprar',
                                description='Conoce el costo de unirte a nosotros.',
                            ),
                            SectionRow(
                                title='🆔 Ser ADI',
                                callback_data='catalogo',
                                description='Qué implica y beneficios de ser ADI.',
                            )
                        ],
                    )
                ]
            )
        )
        logger.info("Producto enviado: %s a %s", response, from_number)
        return {
            "from": from_number,
            "to": to_number,
            "body": response
        }
    elif message == "soyadi":
        response = wa.send_message(
            to=to_number,
            header='Menú Vianney',
            text='Selecciona una de las siguientes opciones del menú para explorar todo lo que tenemos para ti.',
            buttons=SectionList(
                button_title='Soy ADI',
                sections=[
                    Section(
                        title='Menú',
                        rows=[
                            SectionRow(
                                title='👩 Mi Vianney',
                                callback_data='consulta',
                                description='Consulta todo sobre tu cuenta ADI.',
                            ),
                            SectionRow(
                                title='💳 CrediADI',
                                callback_data='ventas',
                                description='Información sobre tu crédito.',
                            ),
                            SectionRow(
                                title='📲 Tarjeta Digital',
                                callback_data='estatus',
                                description='Accede a tu tarjeta de forma digital.',
                            ),
                            SectionRow(
                                title='🎁 Promociones',
                                callback_data='comprar',
                                description='Descubre nuestras ofertas actuales.',
                            )
                        ],
                    )
                ]
            )
        )
        logger.info("Producto enviado: %s a %s", response, from_number)
        return {
            "from": from_number,
            "to": to_number,
            "body": response
        }
    else:
        try:
            response_text = get_openai_response(message)
            response = wa.send_message(to=to_number, text=response_text)
            # response = wa.send_message(
            #     to=to_number,
            #     text=response_text,
            #     buttons=[
            #         Button(title='🛒 Ventas', callback_data='ventas'),
            #         Button(title='🔍 Consultas', callback_data='consultas'),
            #         Button(title='👩 Soy ADI', callback_data='soyadi'),
            #     ]
            # )
            return {
                "from": from_number,
                "to": to_number,
                "body": response
            }
        except WhatsAppError as e:
            logger.error("Error al enviar mensaje: %s", e)
            return {"statusCode": 500, "body": str(e)}


# env
# OPENAI_API_KEY	
# WP_TOKEN

# layer 
# arn:aws:lambda:us-east-2:315068324448:layer:openai_pywa:1