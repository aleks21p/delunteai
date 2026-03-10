# delunteai

Small Discord AI bot. This repo no longer contains secrets — they are loaded from a local `.secrets` file.

## Setup

- Copy the example secrets file and edit it with your real token:

```bash
cp .secrets.example .secrets
# edit .secrets and set TOKEN=your_discord_token_here
```

- Install dependencies (use your venv):

```bash
python -m pip install -r requirements.txt
# or use your existing virtualenv
```

## Run

- Run the Discord bot:

```bash
python chatbot.py
```

- Run the web API under Uvicorn (recommended):

```bash
# using the module's ASGI app
uvicorn webai:asgi_app --host 0.0.0.0 --port 5050

# or run directly (this will start uvicorn)
python webai.py
```

## Secrets and security

- `.secrets` is ignored by git (`.gitignore`) and kept local. Do NOT commit it.
- The repo previously contained a leaked Discord token; it was removed from history and the cleaned branch was force-pushed. Rotate the token in the Discord Developer Portal immediately and update `.secrets`.

## Files

- `chatbot.py` — main bot using secrets from `.secrets` or `TOKEN` env var.
- `.secrets.example` — example secrets template.

If you want, I can also add a `requirements.txt` or a GitHub Actions secret-rotation reminder.
## Development tooling

- Install developer tools and pre-commit hooks:

```bash
python -m pip install -r requirements.txt
pre-commit install
```

- The repo includes a `.pre-commit-config.yaml` with `detect-secrets`. After installing, run:

```bash
pre-commit run --all-files
```
