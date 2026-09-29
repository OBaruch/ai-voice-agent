# Archive

Historical files kept for reference. They are **not** part of the running application.

| File | What it is |
|---|---|
| `tets2.py` | The first prototype (10 April 2025, commit `7442ec5`), originally named `main.py`. It uses OpenAI `gpt-3.5-turbo` for replies and OpenAI `tts-1` for speech, and saves an MP3 to `/tmp`. It was replaced by the Twilio + Hugging Face version in `src/main.py`. |

The file name and contents are unchanged. The name `tets2.py` is original, possibly a typo of
`test2.py`. The file cannot run with the root `requirements.txt` because `openai` is
not listed, and it mixes OpenAI SDK versions. See
[../docs/code-overview.md](../docs/code-overview.md#archivetets2py).
