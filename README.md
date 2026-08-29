# RAG-Document-Assistant
A fully local RAG-based document assistant using LangChain, Ollama, ChromaDB, Hugging Face embeddings, and PyQt6.

# Gemma (local) integration — README / Integration notes

This document explains how to run a local Gemma LLM for development and how to use the `src/llm/test_gemma.py` helper script included in this PR.

> Summary  
> The repository includes a small helper script that demonstrates calling a local Gemma LLM via the ChatOllama adapter. This guide covers prerequisites, installation, running the model locally, usage of the script, troubleshooting, and recommended CI/testing practices.

## Prerequisites
- Python 3.8+ (use the same interpreter used by the repo)
- Repo dependencies installed (the script uses the `langchain_ollama` integration)
- A local runtime that provides the `gemma4:latest` model (the PR uses an Ollama-style integration; if you use a different local runner, adjust commands accordingly)

## Recommended dependency changes
Add the Python dependency used by the script to your project:
- requirements.txt: add `langchain-ollama` (or the correct package name you use in your project)
- Or add the equivalent to `pyproject.toml` / Poetry / Pipenv

Example:
```bash
# if you use requirements.txt
echo "langchain-ollama>=0.1.0" >> requirements.txt
pip install -r requirements.txt
```

(Adjust the package name and version to match your environment / package manager.)

## Install / Prepare a local Gemma runtime
This guide assumes you use Ollama as the local runtime (the script imports from `langchain_ollama`). If you use another runtime, consult that runtime's docs.

1. Install Ollama (or other runtime) — see the runtime's official docs (e.g., https://ollama.ai).
2. Pull / install the Gemma model you need (example placeholder):
```bash
# example: using Ollama to pull the gemma model (replace with actual runtime command if different)
ollama pull gemma4:latest
```
3. Ensure the runtime is running or available. Some runtimes start a daemon automatically; others require an explicit `serve` or `start` command:
```bash
# examples — replace with the correct command for your runtime
ollama serve
# or
ollama run gemma4:latest
```

If your runtime uses a custom host/port, note the settings so the adapter can discover it (see Troubleshooting / Configuration below).

## Usage — running the included script
1. Install Python dependencies for the repo:
```bash
pip install -r requirements.txt
```

2. Run the script:
```bash
python src/llm/test_gemma.py
```

3. Example interactive session:
- The script will prompt: `Ask Gemma:`  
- Type a question and press Enter. The script prints the model response.

If you prefer a one-shot invocation you can adapt the script to accept a command-line argument.

## Example (what the script does)
- `create_llm()` constructs a ChatOllama client for `model="gemma4:latest"`.
- `ask_llm(llm, question)` sends the prompt and returns the response text.
- `main()` prompts for input and prints the returned text.

## Troubleshooting
- SyntaxError at import or function definitions:
  - Ensure the Python file uses valid function annotation syntax (use `->` for return annotations).
- ModuleNotFoundError: `langchain_ollama`:
  - Install the dependency and ensure the virtual environment used by the project is active.
- Model not found:
  - Confirm you pulled the correct model name/tag (e.g., `gemma4:latest`) in your local runtime.
- Connection refused / timeout:
  - Ensure the runtime daemon is running and listening on the expected port/host.
  - If the runtime uses authentication or a non-standard URL, configure the adapter or environment variables accordingly.
- Unexpected response shape:
  - Different client libraries or versions may return responses as lists or objects with different fields. Update the `ask_llm` function to extract the text correctly for your client version.

## Security and privacy notes
- Local models reduce external network exposure, but be mindful of:
  - Logging: avoid logging sensitive user data.
  - File I/O: don't write secrets to disk.
  - Shared machines: ensure only authorized users can access the runtime.
- If you later enable remote LLM backends, ensure secrets (API keys) are stored securely (e.g., environment variables, secret managers).

## Testing & CI recommendations
- Unit tests:
  - Add a unit test that mocks the ChatOllama client to verify `ask_llm` extracts text correctly.
- Integration tests:
  - Add an optional integration test that runs only when a specific environment variable is present (e.g., `RUN_GEMMA_INTEGRATION=1`) so CI won't fail for maintainers who can't run the local model.
- CI job example (pseudo):
```yaml
# .github/workflows/gemma-integration.yml (optional)
name: Gemma integration (optional)
on: [workflow_dispatch]
jobs:
  gemma:
    runs-on: ubuntu-latest
    if: env.RUN_GEMMA_INTEGRATION == '1'
    steps:
      - uses: actions/checkout@v3
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Run integration test
        env:
          RUN_GEMMA_INTEGRATION: ${{ secrets.RUN_GEMMA_INTEGRATION }}
        run: pytest tests/test_gemma_integration.py
```
- Use gating so integration runs only on-demand or when maintainers opt in.

## Recommended follow-ups (author)
1. Add the runtime dependency to the project dependency file.
2. Add a README snippet linking to this doc.
3. Add a unit test that mocks the LLM client.
4. Consider improving the script with:
   - configurable model name and timeout via CLI args or env vars
   - better error handling and logging
   - non-interactive mode for scripted usage

## Contact / Notes
If you need, I can:
- add this file to the repo as `docs/GEMMA_INTEGRATION.md` and open a commit/PR, or
- update the `requirements.txt` and push a follow-up commit that fixes the script (annotations, error handling), or
- create starter unit + integration test files.
