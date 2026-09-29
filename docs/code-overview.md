# Code Overview

This is a file-by-file explanation of the original code. The code itself has not been
changed. Line numbers refer to the files as they are in this repository.

## `src/main.py`

This is the final implementation, at commit `116d9fb` (12 April 2025). It is 61 lines long.

### Imports and app

```python
from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
import requests
import os

app = FastAPI()
```

`app` is the ASGI application that Uvicorn serves (`main:app`).

### `POST /twilio-voice` → `twilio_voice(request: Request)`

This is the entry point Twilio calls when a call comes in. It ignores the request and returns
fixed TwiML:

- `<Gather input="speech" action="/twilio-process" method="POST" timeout="10">`. Twilio
  listens for speech and posts the transcription to `/twilio-process`.
  - Inside it: `<Say voice="alice" language="es-MX">Hola, ¿en qué puedo ayudarte hoy?</Say>`
- After the gather: `<Say …>Lo siento, no escuché nada.</Say>`. This runs only if nothing was
  captured.

The response type is `application/xml`.

### `POST /twilio-process` → `process_speech(SpeechResult: str = Form(...))`

This endpoint receives Twilio's transcription as the form field `SpeechResult`. The field is required,
so FastAPI returns 422 if it is missing. Form parsing needs `python-multipart`.

The steps are:

1. Logs `Texto detectado por Twilio STT: <text>` to stdout.
2. Reads `HUGGINGFACE_TOKEN` from the environment and builds an `Authorization: Bearer` header.
3. Builds the prompt:
   ```
   Eres un experto colista, mnsaje del cliente::

   Usuario: <SpeechResult>
   Asistente:
   ```
4. Sends the prompt to
   `https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct` with
   `max_new_tokens=150`, `temperature=0.7`, and `do_sample=True`.
5. If the response is OK (2xx), it takes `response_json[0]['generated_text']`, keeps the text after the last
   `"Asistente:"`, and strips whitespace. Otherwise it uses a fallback message:
   *"Lo siento, hubo un error al procesar tu solicitud."*
6. Returns TwiML `<Say voice="alice" language="es-MX">{respuesta}</Say>`.

### Observed behavior (verified during reorganization)

- `uvicorn main:app --app-dir src` starts without errors when using the packages in `requirements.txt`.
- `POST /twilio-voice` returns the TwiML above with status 200.
- `POST /twilio-process` with no network access to Hugging Face raises
  `requests.exceptions.ProxyError`, and the server returns **HTTP 500**. The fallback message
  only covers non-2xx HTTP responses, not connection errors.

### Dependencies used

`fastapi`, `requests`, and `python-multipart` (implicitly, through `Form`). `uvicorn` is used as the server.
These match `requirements.txt` exactly.

## `archive/tets2.py`

This is the first prototype, committed as `main.py` in `7442ec5` (10 April 2025). It was renamed to
`tets2.py` 13 minutes later, when a minimal Railway test replaced it. It is 55 lines long.

It is kept for historical reference. **It cannot run with the current
`requirements.txt`** because `openai` is not listed. It also mixes OpenAI SDK styles, as noted below.

### Structure

- `openai.api_key = os.getenv("OPENAI_API_KEY")`
- `class TwilioSpeechEvent(BaseModel)` with optional `SpeechResult` and `CallSid`.
- `POST /twilio-voice` → `receive_twilio_event(event: TwilioSpeechEvent)`:
  1. Returns `{"error": "No se recibió transcripción"}` if `SpeechResult` is empty.
  2. **Step 1** (`# Paso 1`): calls `openai.ChatCompletion.create(model="gpt-3.5-turbo")` with
     the system prompt *"Eres un agente telefónico amable."*
  3. **Step 2** (`# Paso 2`): calls `openai.Audio.speech.create(model="tts-1", voice="nova")`.
  4. **Step 3** (`# Paso 3`): writes the audio to `/tmp/{CallSid}.mp3`.
  5. Returns JSON `{"response_text", "audio_file"}`.
- The closing comments say the prototype needs environment variables and can be run with
  `uvicorn main:app --reload`.

### Notes (not fixed)

- `openai.ChatCompletion` belongs to the pre-1.0 OpenAI SDK. `openai.Audio.speech` does
  not exist in that SDK. Speech synthesis is `client.audio.speech` in SDK ≥ 1.0. The two
  calls cannot both work with a single SDK version.
- Twilio sends webhooks as form data, but this endpoint expects a JSON body.
- It returns JSON rather than TwiML, so Twilio could not play the result directly.

## `requirements.txt`

```
fastapi
uvicorn[standard]
requests
python-multipart
```

No versions are pinned. `requests` was added in `89d3189`, and `python-multipart` was added in `d79d797`.
The second addition was needed because `/twilio-process` reads form data.
