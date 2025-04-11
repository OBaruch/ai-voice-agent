from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import requests
import os

app = FastAPI()

# Configura tu API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Idealmente se guarda como variable de entorno

class TwilioSpeechEvent(BaseModel):
    SpeechResult: str = None
    CallSid: str = None

@app.post("/twilio-voice")
async def receive_twilio_event(event: TwilioSpeechEvent):
    if not event.SpeechResult:
        return {"error": "No se recibió transcripción"}

    user_text = event.SpeechResult
    print(f"[Twilio] Call {event.CallSid}, text: {user_text}")

    # Paso 1: Procesa el texto con GPT
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un agente telefónico amable."},
            {"role": "user", "content": user_text}
        ]
    )
    response_text = gpt_response.choices[0].message['content']

    # Paso 2: Convierte el texto a voz (TTS OpenAI API)
    tts_response = openai.Audio.speech.create(
        model="tts-1",
        voice="nova",
        input=response_text
    )

    # Paso 3: Guarda la respuesta de voz en un archivo temporal
    audio_path = f"/tmp/{event.CallSid}.mp3"
    with open(audio_path, "wb") as f:
        f.write(tts_response.content)

    # Aquí podrías subir ese audio a un bucket y devolver la URL a Twilio para reproducir

    return {
        "response_text": response_text,
        "audio_file": audio_path
    }

# Requiere tener definidas variables de entorno o pasar claves manualmente
# Puedes probarlo localmente con:
# uvicorn main:app --reload
