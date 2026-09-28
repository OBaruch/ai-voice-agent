# Plan

This document has two parts:

- **Part A** reconstructs how the original implementation was built in April 2025. The steps
  come from the git history.
- **Part B** is the plan for the 2026 repository reorganization. It changed documentation and
  layout only, not code.

Related: [intent.md](intent.md) · [spec.md](spec.md) ·
[development-history.md](../development-history.md)

---

## Part A: Original implementation (retrospective, April 2025)

| Step | Goal | Result | Commits |
|---|---|---|---|
| A1 | Prototype the idea with OpenAI (chat + TTS) | Built, then set aside. It returned JSON and MP3 files that Twilio could not use directly. Now in `archive/tets2.py` | `7442ec5` |
| A2 | Check that FastAPI can be deployed on Railway | `GET /hello` smoke test | `acd9dd5`, `0da77ea`, `7d8a5bf`, `9a4300e` |
| A3 | Use Twilio for speech-to-text and text-to-speech, and call an LLM for the reply | Two TwiML endpoints plus the Hugging Face Mistral model | `7e89785`, `89d3189`, `d79d797` |
| A4 | Make it sound natural in Spanish | `language="es-MX"`, `Usuario/Asistente` framing, reply extraction | `ffa45c8` |
| A5 | Compare models | Mistral 7B → Zephyr 7B → Llama 3 8B Instruct (final) | `ffa45c8`, `107abe2`, `ed655e3`, `9310fde` |
| A6 | Make the conversation more reliable | `timeout="10"` on `<Gather>` | `ed655e3` |
| A7 | Try a business persona | Optical-store system prompt, later replaced | `ed655e3`, `116d9fb` |

Planned next steps that were not built:

- Upload the generated audio and let Twilio play it by URL (comment in `archive/tets2.py`).
- Multi-turn conversation. This is inferred from the README's "real-time voice conversations".

---

## Part B: Repository reorganization (2026)

### Principle

Update the repository, not the project. Source files must stay byte-identical.

### Constraints

- Do not edit `src/main.py`, `archive/tets2.py`, or `requirements.txt`.
- Do not add Docker, CI/CD, linters, formatters, test frameworks, or build tooling.
- Do not invent context. Label each statement as Confirmed, Inferred, or Unknown.

### Tasks

| # | Task | Output | Status |
|---|---|---|---|
| B1 | Collect all sources: files and full git history | Context notes | Done |
| B2 | Classify the project origin | Personal Project / Proof of Concept (inferred) | Done |
| B3 | Move the current code to `src/` with `git mv` | `src/main.py` | Done |
| B4 | Move the superseded prototype to `archive/` with `git mv` | `archive/tets2.py`, `archive/README.md` | Done |
| B5 | Confirm the contents are unchanged (`git hash-object` before and after) | Identical blob hashes | Done |
| B6 | Smoke-test the moved app: `uvicorn main:app --app-dir src`, then `POST /twilio-voice` | 200 + TwiML | Done |
| B7 | Write the README and `docs/` (context, architecture, code overview, history, improvements) | Markdown docs | Done |
| B8 | Write the SDLC artifacts from the existing code | `intent.md`, `spec.md`, `plan.md` | Done |
| B9 | Add `AGENTS.md` with preservation rules for future contributors and agents, plus a minimal Python `.gitignore` | Root files | Done |
| B10 | Open a pull request for review | PR | Done |

### Verification

```bash
# Source blobs must match the pre-reorganization versions
git diff --stat <base>..HEAD -M -- src archive requirements.txt   # only renames, 0 line changes
uvicorn main:app --app-dir src &
curl -s -X POST localhost:8000/twilio-voice                      # returns TwiML
```

### Deployment note

Railway (or any platform) was previously set up to run `main.py` from the repository root.
After this reorganization, the start command must be `uvicorn main:app --app-dir src`
(plus `--host 0.0.0.0 --port $PORT` or similar for the platform). This project is not
known to be deployed currently.

### Future work (out of scope)

Any modernization belongs in a separate effort, with its own intent, spec, and plan.
See [possible-improvements.md](../possible-improvements.md) for starting points.
