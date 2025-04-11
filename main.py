from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
import requests
import os

app = FastAPI()

@app.post("/twilio-voice")
async def twilio_voice(request: Request):
    response = """
    <Response>
        <Gather input="speech" action="/twilio-process" method="POST">
            <Say voice="alice">Hola, ¿en qué puedo ayudarte hoy?</Say>
        </Gather>
        <Say>Lo siento, no escuché nada.</Say>
    </Response>
    """
    return Response(content=response, media_type="application/xml")

@app.post("/twilio-process")
async def process_speech(SpeechResult: str = Form(...)):
    print(f"Texto detectado por Twilio STT: {SpeechResult}")

    # Consulta a Hugging Face Inference API
    hf_token = os.getenv("HUGGINGFACE_TOKEN")  # Asegúrate de tener esta variable en Railway
    headers = {
        "Authorization": f"Bearer {hf_token}"
    }
    payload = {
        "inputs": SpeechResult,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7
        }
    }
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    hf_response = requests.post(url, headers=headers, json=payload)

    if hf_response.ok:
        response_json = hf_response.json()
        respuesta = response_json[0]['generated_text']
    else:
        respuesta = "Lo siento, hubo un error al procesar tu solicitud."

    response = f"""
    <Response>
        <Say voice="alice">{respuesta}</Say>
    </Response>
    """
    return Response(content=response, media_type="application/xml")
