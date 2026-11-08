#!/usr/bin/env bash
# Turn out/merged into an Ollama model called "veya-tutor". Run on your Mac (needs git, python, ollama).
set -e
[ -d llama.cpp ] || git clone --depth 1 https://github.com/ggml-org/llama.cpp
pip install -r llama.cpp/requirements/requirements-convert_hf_to_gguf.txt   # if this path changed, follow llama.cpp's README
python llama.cpp/convert_hf_to_gguf.py out/merged --outfile out/veya-tutor-f16.gguf --outtype f16
cp Modelfile out/Modelfile
cd out
ollama create veya-tutor -f Modelfile          # smaller file: ollama create veya-tutor -q q4_K_M -f Modelfile
echo "Done. Test: ollama run veya-tutor   Then add VEYA_TUTOR_MODEL=veya-tutor to Veya's .env and restart."
