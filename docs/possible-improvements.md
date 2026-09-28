# Possible Improvements

> **None of these changes were applied.** The source code is kept exactly as it was
> written in April 2025 to preserve the original implementation. This list records
> observations that could guide a future, separate modernization effort.

## Correctness and robustness (`src/main.py`)

1. **Unhandled network errors.** `requests.post` exceptions (timeouts, DNS failures,
   proxy errors) are not caught, so Twilio receives an HTTP 500. This was verified locally.
   Only non-2xx responses fall back to the error message.
2. **No request timeout** on `requests.post`. A slow model can take longer than Twilio's
   webhook time limit.
3. **Unescaped XML.** The model's reply is inserted into TwiML with an f-string. Characters
   such as `<` or `&` can produce invalid XML. Using `twilio.twiml.voice_response` or
   `xml.sax.saxutils.escape` would fix this.
4. **Fragile response parsing.** The code assumes `response_json[0]['generated_text']`. Hugging Face
   also returns objects like `{"error": ..., "estimated_time": ...}` while a model is loading,
   sometimes with a 2xx status. Depending on the case, this could cause a `KeyError` or `TypeError`.
5. **Missing token.** If `HUGGINGFACE_TOKEN` is not set, the header becomes `Bearer None`, and the
   code does not detect this.
6. **Blocking call in an async handler.** `requests` blocks the event loop. `httpx.AsyncClient`
   or a plain `def` handler would avoid this.

## Conversation design

7. **Single turn only.** Adding another `<Gather>` after the reply, and storing history by
   `CallSid`, would support real conversations.
8. **Prompt format.** Llama 3 Instruct expects its chat template (`<|start_header_id|>…`)
   or a chat-completion endpoint. Plain `Usuario:/Asistente:` text works less reliably.
9. **Prompt content.** The final prompt contains typos ("mnsaje") and an unclear
   term ("colista"). The more detailed optical-store prompt from commit `ed655e3` is a
   better example of a domain prompt.
10. **Voice quality.** `alice` is Twilio's legacy voice. Twilio's newer Polly/Google
    voices, or `<Play>` with generated audio as the prototype planned, could sound better.

## Security

11. **No Twilio signature validation** (`X-Twilio-Signature`), so anyone can call the
    endpoints and use up the Hugging Face quota.
12. **Prompt injection.** Caller speech goes straight into the prompt without any guardrails.

## Platform and dependencies

13. **Unpinned dependencies.** `requirements.txt` has no versions, so builds can change
    over time.
14. **Hugging Face endpoint changes.** The classic `api-inference.huggingface.co/models/<id>`
    endpoint and the availability of gated models such as Llama 3 have changed since 2025.
    A modern version should use Hugging Face's current Inference Providers or router API. Check the
    current documentation.
15. **Archived prototype.** `archive/tets2.py` would need `openai` in its dependencies and
    a single consistent SDK version to run.

## Engineering practices

16. There are no tests. FastAPI's `TestClient` could check the TwiML for both endpoints,
    with the Hugging Face call mocked.
17. Logging uses `print`. Structured logging with `CallSid` would make debugging easier.
18. Configuration such as the model URL, voice, language, and generation parameters is hard-coded. It could
    come from environment variables.
19. `Request` is imported and received in `twilio_voice` but never used.
