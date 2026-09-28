# Development History

This history is reconstructed from the git log. All commits are by Baruch Lopez, and the
timestamps are UTC-6. The history shows how the design changed over about 36 hours.

| # | Commit | Date | Change |
|---|---|---|---|
| 1 | `eac85e7` | 2025-04-10 23:21 | Initial commit: `README.md` and MIT `LICENSE`. |
| 2 | `7442ec5` | 2025-04-10 23:21 | **Prototype v0**: `main.py` using OpenAI `gpt-3.5-turbo` + `tts-1`, which saves an MP3 to `/tmp` and returns JSON. *(Now `archive/tets2.py`.)* |
| 3 | `acd9dd5` | 2025-04-10 23:24 | `test.py`: minimal FastAPI `GET /hello` → *"Hola desde Railway con FastAPI 🚀"*. |
| 4 | `0da77ea` | 2025-04-10 23:31 | Prototype `main.py` renamed to `tets2.py`. |
| 5 | `7d8a5bf` | 2025-04-10 23:31 | `test.py` renamed to `main.py` (the Railway smoke test becomes the entry point). |
| 6 | `9a4300e` | 2025-04-10 23:33 | `requirements.txt` created (`fastapi`, `uvicorn[standard]`). |
| 7 | `7e89785` | 2025-04-11 00:02 | **Twilio + Hugging Face v1**: TwiML `/twilio-voice` and `/twilio-process`, with `mistralai/Mistral-7B-Instruct-v0.1` and the raw speech text as the prompt. |
| 8 | `89d3189` | 2025-04-11 00:09 | Adds `requests`. |
| 9 | `d79d797` | 2025-04-11 00:11 | Adds `python-multipart` (needed for `Form`). |
| 10 | `ffa45c8` | 2025-04-11 00:33 | Spanish voice (`language="es-MX"`) on every `<Say>`. Switches to `HuggingFaceH4/zephyr-7b-beta` with `Usuario:/Asistente:` framing, `max_new_tokens` 100→150, `do_sample`, and reply extraction after `Asistente:`. |
| 11 | `2ba8c2f` | 2025-04-11 00:34 | Greeting personalized for a specific person. |
| 12 | `107abe2` | 2025-04-11 00:41 | Switches the model to `meta-llama/Meta-Llama-3-8B-Instruct`. |
| 13 | `ed655e3` | 2025-04-11 00:50 | Adds `timeout="10"` to `<Gather>` and restores the generic greeting. Adds a **persistent context prompt** for an optical-store / ophthalmology assistant. Model temporarily back to Zephyr. |
| 14 | `9310fde` | 2025-04-11 00:55 | Model back to Llama 3 8B Instruct. |
| 15 | `116d9fb` | 2025-04-12 11:52 | Replaces the optical-store prompt with *"Eres un experto colista, mnsaje del cliente::"*. **Final state.** |

## Phases

1. **OpenAI prototype** (commit 2). The idea was GPT for reasoning and OpenAI TTS for voice. It was
   dropped quickly, probably because it did not fit Twilio's webhook and TwiML model. That reason
   is *inferred*.
2. **Deployment smoke test** (commits 3–6). The author checked that a FastAPI app runs on Railway.
3. **Twilio-native loop** (commits 7–9). Speech-to-text and text-to-speech moved to Twilio, and only the
   LLM stayed external. The Hugging Face Inference API replaced OpenAI.
4. **Tuning** (commits 10–15). The author changed the language and voice, compared three open models, tried prompt
   framing and a domain-specific system prompt, and added a speech timeout.

## Models tried

| Model | Commits |
|---|---|
| OpenAI `gpt-3.5-turbo` (+ `tts-1`, voice `nova`) | 2 |
| `mistralai/Mistral-7B-Instruct-v0.1` | 7 |
| `HuggingFaceH4/zephyr-7b-beta` | 10, 13 |
| `meta-llama/Meta-Llama-3-8B-Instruct` | 12, 14, 15 (final) |

## 2026 reorganization

The repository was reorganized and documented without changing the code. See
[sdlc/plan.md](sdlc/plan.md#part-b--repository-reorganization-2026).
