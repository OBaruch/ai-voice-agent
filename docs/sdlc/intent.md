# Intent

> **Retrospective artifact.** This intent was written in 2026 from the existing code,
> the original README, and the git history. It records why the project was built, not
> a new direction. Items marked *(Inferred)* are not stated in the original sources.

## Problem

Phone calls are still a main support channel for many businesses. Automating them usually
needs expensive IVR platforms or complex integrations. The question behind this project
was: **can a phone call be connected to an LLM with only a few lines of code?** *(Inferred)*

## Intent statement

Build an *"AI-powered voice call agent … [that] enables real-time voice conversations with
an intelligent assistant"*, aimed at *"smart call automation and custom voice agents"*.
*(Confirmed: original README.)*

## Goals

| ID | Goal | Evidence |
|---|---|---|
| G1 | Answer an incoming phone call automatically and greet the caller in Spanish. | Confirmed (code) |
| G2 | Turn the caller's speech into text. | Confirmed (Twilio `<Gather input="speech">`) |
| G3 | Generate a relevant reply with an LLM. | Confirmed (Hugging Face call) |
| G4 | Speak the reply back to the caller. | Confirmed (Twilio `<Say>`) |
| G5 | Keep costs and infrastructure low: hosted APIs, one small service on a PaaS. | Inferred (move from OpenAI to Hugging Face; Railway) |
| G6 | Allow the assistant's persona to change for a business use case. | Inferred (optical-store prompt experiment) |

## Non-goals (as built)

- Multi-turn dialogue or conversation memory.
- Outbound calling, call transfer, or human hand-off.
- Production concerns: authentication, scaling, monitoring, persistence.
- Custom or neural voices in the final version.

## Users

- **Caller**: a Spanish-speaking person phoning the Twilio number.
- **Operator/author**: sets up Twilio, Railway, and the Hugging Face token, and edits the prompt.

## Success criteria (retrospective)

| Criterion | Status |
|---|---|
| The service starts and returns valid TwiML for an incoming call | **Met** (verified locally in 2026) |
| A caller hears an LLM-generated answer to one spoken question | **Unverified** (depends on Twilio and Hugging Face accounts; no record in the repository) |
| Conversation continues across several turns | **Not met** (not implemented) |

## Constraints

- Minimal code: a single Python file.
- Only hosted third-party services: Twilio and the Hugging Face Inference API.
- Spanish (Mexico) language.

## Related

- Specification: [spec.md](spec.md)
- Plan: [plan.md](plan.md)
- Context: [../project-context.md](../project-context.md)
