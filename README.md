# ai-voice-agent

A small proof of concept for a Spanish-language phone voice assistant. A
[FastAPI](https://fastapi.tiangolo.com/) web service answers
[Twilio](https://www.twilio.com/) Voice webhooks, sends the caller's transcribed
speech to a large language model hosted on the Hugging Face Inference API, and reads
the model's reply back to the caller using Twilio's built-in text-to-speech.

> **Original implementation.** This repository preserves the original implementation of the project. The source code has intentionally not been refactored or modernized in order to retain the historical context and original development approach. The source code represents the original implementation developed as a personal project.

---

## Project Overview

| | |
|---|---|
| **Type** | Personal project, proof of concept *(inferred, see [project context](docs/project-context.md))* |
| **Author** | Baruch Lopez |
| **Developed** | 10–12 April 2025 (from git history) |
| **Language** | Python |
| **Size** | One FastAPI application file (`src/main.py`, 61 lines) plus one archived prototype |
| **Spoken language** | Spanish (Mexico), `es-MX` |
| **License** | [MIT](LICENSE) |

## Project Context

There are no assignment documents, reports or course references in the repository.
All context comes from the code, the original one-line README, the `LICENSE`, and
the git history. That evidence points to a **personal proof of concept**: it was built
by one author over roughly two days, with many small commits that change models and
prompts, and it was set up for deployment on [Railway](https://railway.app/).

See [`docs/project-context.md`](docs/project-context.md) for the evidence and for what
remains unknown.

## Problem Statement

*(Inferred.)* The project checks whether a phone call can be connected to an LLM so a
caller can speak a question and hear an AI-generated answer. It aims to do this with
little code and free or low-cost hosted services.

## Objective

The original README describes the goal as an *"AI-powered voice call agent … [that]
enables real-time voice conversations with an intelligent assistant. Designed for
smart call automation and custom voice agents."*

The code that exists covers one turn of that goal: greet the caller, capture one
utterance, generate one reply, and speak it.

## Repository Structure

```
ai-voice-agent/
├── README.md              ← this file
├── AGENTS.md              ← working rules for contributors and AI coding agents
├── LICENSE                ← MIT, © 2025 Baruch Lopez (original)
├── requirements.txt       ← original Python dependencies (unchanged)
├── .gitignore
├── src/
│   └── main.py            ← original FastAPI app (latest version, unchanged)
├── archive/
│   ├── README.md
│   └── tets2.py           ← earlier OpenAI-based prototype (unchanged, not runnable as-is)
└── docs/
    ├── project-context.md
    ├── architecture.md
    ├── code-overview.md
    ├── development-history.md
    ├── possible-improvements.md
    └── sdlc/
        ├── intent.md      ← why the project exists (retrospective)
        ├── spec.md        ← what the system does (as-built specification)
        └── plan.md        ← how it was built and how this repository was reorganized
```

## Original Implementation

The files in `src/` and `archive/` and the `requirements.txt` file are exactly as the author wrote
them. This includes Spanish comments, typos, unused imports, and known defects. The
2026 reorganization only moved files into folders with `git mv` and added
documentation. Improvement ideas are listed in
[`docs/possible-improvements.md`](docs/possible-improvements.md). **None of them were
applied.**

## Technologies

Confirmed from code and `requirements.txt`:

- **Python**. The minimum version is not specified.
- **FastAPI**: web framework for the webhook endpoints.
- **Uvicorn** (`uvicorn[standard]`): ASGI server.
- **requests**: HTTP client used to call Hugging Face.
- **python-multipart**: lets FastAPI parse Twilio's form-encoded webhook body.
- **Twilio Voice / TwiML**: `<Gather input="speech">` for speech-to-text and `<Say voice="alice">` for text-to-speech.
- **Hugging Face Inference API**: model `meta-llama/Meta-Llama-3-8B-Instruct`.
- **Railway**: mentioned in the history as the deployment platform.

Used only in the archived prototype: **OpenAI API** (`gpt-3.5-turbo`, `tts-1`) and
**Pydantic** models.

> The original README mentions "GPT and TTS". That describes the archived prototype.
> The final implementation uses Llama 3 on Hugging Face and Twilio's own TTS instead.

## How It Works

```
Caller ──phone──▶ Twilio ──POST /twilio-voice──▶ FastAPI  → TwiML: <Gather speech> + greeting
Caller speaks ──▶ Twilio STT ──POST /twilio-process (SpeechResult)──▶ FastAPI
                                   FastAPI ──POST──▶ Hugging Face (Llama 3 8B Instruct)
                                   FastAPI → TwiML: <Say> reply
Twilio TTS ──speaks reply──▶ Caller   (the TwiML ends; the call finishes)
```

1. **`POST /twilio-voice`** returns TwiML. It greets the caller in Spanish (*"Hola, ¿en qué
   puedo ayudarte hoy?"*) and waits up to 10 seconds for speech.
2. Twilio transcribes the speech and posts `SpeechResult` to **`POST /twilio-process`**.
3. The service builds a prompt: a fixed system-style context, then `Usuario: <speech>`, then `Asistente:`.
   It sends the prompt to the Hugging Face Inference API with `max_new_tokens=150` and `temperature=0.7`.
4. The text after the last `Asistente:` in the model output is returned inside a
   `<Say>` element, and Twilio reads it aloud.

See [`docs/architecture.md`](docs/architecture.md) and
[`docs/code-overview.md`](docs/code-overview.md) for details.

## Inputs and Outputs

| Direction | What | Format |
|---|---|---|
| Input | Incoming call webhook from Twilio | HTTP POST (body ignored) |
| Input | Caller transcription `SpeechResult` | `application/x-www-form-urlencoded` |
| Input | `HUGGINGFACE_TOKEN` | Environment variable |
| Output | Call instructions | TwiML (`application/xml`) |
| Output | Transcription log line | stdout (`print`) |

The repository contains no datasets, recordings, or saved outputs.

## Running the Project

These steps were checked during the reorganization. The app starts, and `POST /twilio-voice`
returns the expected TwiML. A full phone call was **not** tested.

```bash
pip install -r requirements.txt
export HUGGINGFACE_TOKEN=<your Hugging Face access token>
uvicorn main:app --app-dir src
```

Before the reorganization, `main.py` was at the repository root and ran as
`uvicorn main:app` (the command given in the prototype's comments).

For a real call, the Twilio phone number's *"A call comes in"* webhook must point to
`https://<public-host>/twilio-voice` using HTTP POST. The repository has no Twilio
configuration, so this step is **inferred** from the code.

> **Caveats (not fixed on purpose):** the endpoint `api-inference.huggingface.co/models/...`
> and access to the Llama 3 model depend on third-party services that may have changed
> since April 2025. Network errors while calling Hugging Face cause an HTTP 500. See
> [`docs/possible-improvements.md`](docs/possible-improvements.md).

## Documentation

- [Project context](docs/project-context.md): origin, evidence, and what is known or unknown
- [Architecture](docs/architecture.md): components and request flow
- [Code overview](docs/code-overview.md): file-by-file explanation
- [Development history](docs/development-history.md): how the code evolved, commit by commit
- [Possible improvements](docs/possible-improvements.md): observations, **not applied**
- SDLC artifacts, reconstructed from the existing code:
  [intent](docs/sdlc/intent.md) · [spec](docs/sdlc/spec.md) · [plan](docs/sdlc/plan.md)
- [Archive](archive/README.md): the earlier prototype

## Historical Note

This repository was later reorganized and documented to make it easier to read and to
preserve the historical context of the original project. The original source code
remains unchanged. The original code dates from April 2025. The documentation was
added in 2026.
