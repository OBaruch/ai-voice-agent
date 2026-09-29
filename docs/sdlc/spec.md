# Specification (as-built)

> **Retrospective artifact.** This spec describes what `src/main.py` actually does at commit
> `116d9fb` (April 2025). It was reverse-engineered in 2026. It does not ask for changes. The
> **Status** column compares the requirement with the original code.

- Intent: [intent.md](intent.md)
- Plan: [plan.md](plan.md)

## 1. System overview

A stateless FastAPI service that Twilio Voice calls through webhooks. It exposes two
`POST` endpoints and depends on one external LLM API.

## 2. Functional requirements

| ID | Requirement | Implementation | Status |
|---|---|---|---|
| FR-1 | On an incoming call, the service returns TwiML that greets the caller in Spanish and listens for speech. | `POST /twilio-voice` → `<Gather input="speech" action="/twilio-process" method="POST" timeout="10">` with `<Say voice="alice" language="es-MX">Hola, ¿en qué puedo ayudarte hoy?</Say>` | Met |
| FR-2 | If no speech is detected, the caller hears an apology. | `<Say …>Lo siento, no escuché nada.</Say>` after `<Gather>` | Met |
| FR-3 | The service accepts the transcription from Twilio. | `POST /twilio-process`, form field `SpeechResult` (required) | Met |
| FR-4 | The service logs the transcription. | `print("Texto detectado por Twilio STT: …")` | Met |
| FR-5 | The service builds a prompt from a fixed context and the caller's text. | `"{context}\n\nUsuario: {text}\nAsistente:"` | Met |
| FR-6 | The service asks an LLM for a reply. | `POST https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct`, `max_new_tokens=150`, `temperature=0.7`, `do_sample=True` | Met (service availability today unverified) |
| FR-7 | The service returns only the assistant's part of the generation. | `generated_text.split("Asistente:")[-1].strip()` | Met |
| FR-8 | The service speaks the reply to the caller in Spanish. | `<Say voice="alice" language="es-MX">{respuesta}</Say>` | Met |
| FR-9 | If the LLM fails, the caller hears an error message. | Only for non-2xx responses. Network exceptions cause HTTP 500 | Partially met |

## 3. Interfaces

### 3.1 `POST /twilio-voice`

- **Request:** any. The body is ignored.
- **Response:** `200`, `Content-Type: application/xml`, fixed TwiML (FR-1, FR-2).

### 3.2 `POST /twilio-process`

- **Request:** `application/x-www-form-urlencoded` with `SpeechResult` (string, required).
  Other Twilio fields are ignored.
- **Response:**
  - `200 application/xml`: `<Response><Say …>{reply or fallback}</Say></Response>`
  - `422`: `SpeechResult` is missing (FastAPI validation)
  - `500`: a network or parsing exception occurred

### 3.3 Outbound: Hugging Face Inference API

- **Auth:** `Authorization: Bearer $HUGGINGFACE_TOKEN`
- **Body:** `{"inputs": <prompt>, "parameters": {"max_new_tokens": 150, "temperature": 0.7, "do_sample": true}}`
- **Expected response:** `[{"generated_text": "<prompt + completion>"}]`

## 4. Configuration

| Name | Source | Required |
|---|---|---|
| `HUGGINGFACE_TOKEN` | Environment | Yes, in practice. The code does not check for it |

Everything else is hard-coded (see [../architecture.md](../architecture.md#configuration)).

## 5. Non-functional characteristics (observed)

| Aspect | As built |
|---|---|
| State | None. Each request is independent |
| Concurrency | Async handlers, but a blocking `requests` call |
| Security | No authentication and no Twilio signature validation |
| Observability | stdout `print` only |
| Dependencies | Unpinned: `fastapi`, `uvicorn[standard]`, `requests`, `python-multipart` |
| Tests | None |

## 6. Acceptance scenarios

These are written as Given/When/Then. They document the expected behavior and were not
automated.

1. **Greeting.** *Given* the service is running, *when* `POST /twilio-voice` is called,
   *then* the response is 200 XML containing `<Gather input="speech"` and the Spanish greeting.
   **Verified manually (2026).**
2. **Reply.** *Given* a valid `HUGGINGFACE_TOKEN` and the model is reachable, *when*
   `POST /twilio-process` is called with `SpeechResult=hola`, *then* the response is 200 XML with a
   `<Say>` containing the model's text. **Not verified** (no network access or credentials).
3. **LLM HTTP error.** *Given* Hugging Face returns a non-2xx status, *then* the `<Say>` contains
   *"Lo siento, hubo un error al procesar tu solicitud."* **Checked by reading the code.**
4. **LLM unreachable.** *Given* no network access, *then* the service returns HTTP 500.
   **Verified manually (2026).**

## 7. Out of scope

Multi-turn conversation, call state, outbound calls, custom TTS, persistence, and
authentication. See [../possible-improvements.md](../possible-improvements.md) for ideas.
None of them are implemented.

## 8. Archived prototype (informative)

`archive/tets2.py` described a different contract. It accepted a JSON body, called OpenAI
chat and TTS, and returned JSON with the file path. That contract was replaced by the one above.
