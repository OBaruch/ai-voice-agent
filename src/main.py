from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
import requests
import os

app = FastAPI()

@app.post("/twilio-voice")
async def twilio_voice(request: Request):
    response = """
    <Response>
        <Gather input="speech" action="/twilio-process" method="POST" timeout="10">
            <Say voice="alice" language="es-MX">Hola, ¿en qué puedo ayudarte hoy?</Say>
        </Gather>
        <Say voice="alice" language="es-MX">Lo siento, no escuché nada.</Say>
    </Response>
    """
    return Response(content=response, media_type="application/xml")

@app.post("/twilio-process")
async def process_speech(SpeechResult: str = Form(...)):
    print(f"Texto detectado por Twilio STT: {SpeechResult}")

    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    headers = {
        "Authorization": f"Bearer {hf_token}"
    }

    # Prompt persistente como contexto de sistema
    prompt_contexto = """
    Eres un experto colista, mnsaje del cliente::
    """

    # Concatenamos contexto + entrada
    full_prompt = f"{prompt_contexto.strip()}\n\nUsuario: {SpeechResult}\nAsistente:"

    payload = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7,
            "do_sample": True
        }
    }

    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    hf_response = requests.post(url, headers=headers, json=payload)

    if hf_response.ok:
        response_json = hf_response.json()
        respuesta = response_json[0]['generated_text'].split("Asistente:")[-1].strip()
    else:
        respuesta = "Lo siento, hubo un error al procesar tu solicitud."

    response = f"""
    <Response>
        <Say voice="alice" language="es-MX">{respuesta}</Say>
    </Response>
    """
    return Response(content=response, media_type="application/xml")

