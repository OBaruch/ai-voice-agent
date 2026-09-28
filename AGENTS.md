# AGENTS.md

These are working rules for anyone changing this repository, whether human or AI coding agent.

## What this repository is

This is a historical proof of concept from April 2025: a Twilio voice webhook that sends caller
speech to an LLM on Hugging Face and speaks the reply. Start with [README.md](README.md). The
SDLC artifacts are in [docs/sdlc/](docs/sdlc/): [intent](docs/sdlc/intent.md),
[spec](docs/sdlc/spec.md), [plan](docs/sdlc/plan.md).

## Hard rules

1. **Do not modify the original code.** `src/main.py`, `archive/tets2.py`, and
   `requirements.txt` are preserved as written. Do not reformat them, fix typos or bugs in them, or
   bump their dependencies.
2. **Documentation must be honest.** Label claims as *Confirmed*, *Inferred*, or *Unknown*.
   Do not invent history, deployments, or results.
3. **No added infrastructure** (containers, CI, linters, test frameworks) unless a
   modernization effort is explicitly started.
4. **Improvement ideas** go in [docs/possible-improvements.md](docs/possible-improvements.md)
   and are not applied.

## Starting a modernization

To evolve the project, begin with a new intent, spec, and plan, for example under
`docs/sdlc/<effort-name>/`. Keep the original implementation available unchanged, for example
in `archive/` or at a git tag, so that its history is preserved.

## Useful commands

```bash
pip install -r requirements.txt
HUGGINGFACE_TOKEN=... uvicorn main:app --app-dir src
curl -s -X POST localhost:8000/twilio-voice
```
