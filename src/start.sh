# start.sh
#!/bin/bash

# Download the model if needed
python3 /download_model.py

# Start VLLM instance with corrected parameters
python3 -m vllm.entrypoints.openai.api_server \
  --model /models/Lumo-8B-Instruct-FT-Q4_0.gguf \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype float16 \
  --max-num-batched-tokens 32768 \
  --max-model-len 32768 \
  --max-num-seqs 512 \
  --gpu-memory-utilization 0.95 \
  --quantization awq
