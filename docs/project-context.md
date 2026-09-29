# Project Context

This document gathers everything the repository says about where the project came
from. Each statement is labelled:

- **Confirmed**: directly supported by a file, the code, or git metadata.
- **Inferred**: a reasonable conclusion from the evidence, but not stated anywhere.
- **Unknown**: the repository does not contain enough information.

## Sources available

The repository contains no PDF, Word, PowerPoint, images, diagrams, notebooks,
datasets, or configuration files. The only sources are:

| Source | Content |
|---|---|
| `README.md` (original) | One paragraph: *"AI-powered voice call agent using Twilio, GPT, and TTS…"* |
| `LICENSE` | MIT, *Copyright (c) 2025 Baruch Lopez* |
| `main.py` → `src/main.py` | Final implementation (FastAPI + Twilio + Hugging Face) |
| `tets2.py` → `archive/tets2.py` | Earlier prototype (FastAPI + OpenAI) |
| `requirements.txt` | `fastapi`, `uvicorn[standard]`, `requests`, `python-multipart` |
| Git history | 15 commits, 10–12 April 2025, one author |

## Classification

**Project origin: Personal Project / Proof of Concept** *(Inferred)*

Evidence:

- Confirmed: one author (Baruch Lopez), who also holds the copyright in `LICENSE`.
- Confirmed: no course, university, assignment, or instructor is mentioned anywhere.
- Confirmed: the work was done in about two days (10 April 2025 23:21 to 12 April 2025
  11:52, UTC-6). There were many small edits to model names and prompts in the GitHub editor.
- Confirmed: the first deployed test was a "hello world" endpoint returning
  *"Hola desde Railway con FastAPI 🚀"*. A later comment says
  *"Asegúrate de tener esta variable en Railway"*. Railway was the deployment target.
- Inferred: the short timeline, trial-and-error commits, and switches between free
  hosted models suggest a quick personal experiment. It does not look like graded coursework
  or a production system.

## Objective

- Confirmed (original README): build an *AI-powered voice call agent* that enables
  *real-time voice conversations with an intelligent assistant*, aimed at *smart call
  automation and custom voice agents*.
- Confirmed (code): the final version does one conversational turn in Spanish.
- Inferred: the author wanted to try a phone call → LLM → speech loop without paying for
  OpenAI. The prototype used OpenAI, and the final version uses free or open models on Hugging Face.

## Use-case experiments

The history shows several system prompts tried in sequence (see
[development-history.md](development-history.md)):

1. No system prompt, only `Usuario:` / `Asistente:` framing.
2. A detailed prompt for a **virtual assistant for an optical store chain and
   ophthalmology specialists**. It guides callers toward booking an appointment, picking up
   a free monthly lens-cleaning kit, or visiting the store to buy. It also used a
   personalized greeting.
3. The final committed prompt: *"Eres un experto colista, mnsaje del cliente::"*.

- Confirmed: the three prompts above existed.
- Unknown: whether the optical-store scenario was for a real business, a demo, or a
  hypothetical example. The meaning of "colista" in the final prompt is also unknown.
  It may be a typo, and the repository does not explain it.

## Scope

- In scope (Confirmed): inbound call handling, speech capture through Twilio, one LLM
  reply, and speech playback through Twilio.
- Out of scope / not implemented (Confirmed): multi-turn conversation, conversation
  memory, outbound calls, authentication or Twilio signature validation, persistence,
  tests, custom TTS voices in the final version.

## Unknowns

- Whether the service was ever connected to a real Twilio number and tested with a phone call.
  The history suggests it was: the timeout was added and the greeting was changed, which fits
  live testing. This cannot be confirmed.
- The Python version used.
- Why the prototype file is named `tets2.py`. It may be a typo of `test2.py`.
- Whether any follow-up work happened outside this repository.
