from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from translate import Translator

# chat = ChatOpenAI(openai_api_key="")

def detect_language(obj):
    messages = [
            SystemMessage(
                content="You are a helpful assistant that detects language of the text in the JSON object. You return only the language name."
            ),
            HumanMessage(content=str(obj)),
        ]
    result = chat.invoke(messages)
    language = result.content
    return language


language_short_form = {'English': 'en', 'German': 'de', 'French': 'fr', 'Greek': 'el', 'Croatian': 'hr', 'Polish': 'pl', 'Czech': 'cs', 'Russian': 'ru', 'Swedish': 'sv', 'Norway': 'no', 'Slovak': 'sk', 'Dutch': 'nl'}

def translate_object(obj, from_language, to_language):
    try:
        batch_messages = [
                [
                    SystemMessage(
                        content=f"You are a helpful assistant that translates the text from {from_language} to {to_language} language."
                    ),
                    HumanMessage(content=str(obj["property_title"])),
                ],
                [
                    SystemMessage(
                        content=f"You are a helpful assistant that translates the text from {from_language} to {to_language} language."
                    ),
                    HumanMessage(content=str(obj["property_description"])),
                ],
            ]
        result = chat.generate(batch_messages)
        generations = result.generations
        translator = Translator(from_lang=language_short_form[from_language], to_lang=language_short_form[to_language])
        content = {
                "oib_number": translator.translate(str(obj["oib_number"])) if obj["oib_number"] else None,
                "property_title": generations[0][0].text,
                "property_description": generations[1][0].text,
                "property_type": translator.translate(str(obj["property_type"])) if obj["property_type"] else None,
                "property_status": translator.translate(str(obj["property_status"])) if obj["property_status"] else None,
                "location": translator.translate(str(obj["location"])) if obj["location"] else None,
                "bedrooms": translator.translate(str(obj["bedrooms"])) if obj["bedrooms"] else None,
                "bathrooms": translator.translate(str(obj["bathrooms"])) if obj["bathrooms"] else None,
                "floors": translator.translate(str(obj["floors"])) if obj["floors"] else None,
                "garage": translator.translate(str(obj["garage"])) if obj["garage"] else None,
                "area": translator.translate(str(obj["area"])) if obj["area"] else None,
                "size": translator.translate(str(obj["size"])) if obj["size"] else None,
                "property_price": translator.translate(str(obj["property_price"])) if obj["property_price"] else None,
                "address": translator.translate(str(obj["address"])) if obj["address"] else None,
                "country": translator.translate(str(obj["country"])) if obj["country"] else None,
                "city": translator.translate(str(obj["city"])) if obj["city"] else None,
                "state": translator.translate(str(obj["state"])) if obj["state"] else None,
                "zipcode": translator.translate(str(obj["zipcode"])) if obj["zipcode"] else None,
                "neighborhood": translator.translate(str(obj["neighborhood"])) if obj["neighborhood"] else None,
            }
        return content
    except Exception as e:
        print(e)
        return None
