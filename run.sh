#!/bin/bash
# Mac/Linux: one command for setup + start (for YOU, on your own computer).
# Ollama is the engine that runs the AI model. It must run on the computer that runs this server.
# People who use a hosted Veya in their browser never install Ollama.
cd "$(dirname "$0")"
[ -d venv ] || python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
if ! curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  echo "Starting Ollama..."
  if [ "$(uname)" = "Darwin" ]; then open -a Ollama 2>/dev/null || (ollama serve >/dev/null 2>&1 &); else (ollama serve >/dev/null 2>&1 &); fi
  for i in $(seq 1 30); do curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1 && break; sleep 1; done
fi
ollama pull qwen3:8b && ollama pull nomic-embed-text
[ -f veya.db ] || { echo "Pehla user banao:"; read -p "Naam: " n; python main.py create-user "$n"; }
export VEYA_MODEL="${VEYA_MODEL:-qwen3:8b}" VEYA_THINK="${VEYA_THINK:-0}"
echo "Dashboard: http://127.0.0.1:8000"
uvicorn main:app --port 8000
