# run.sh
# ===== run.sh =====
#!/bin/bash

# Build the Docker image
docker build . -t vllm-gguf

# Run the container
docker run --gpus all \
  --shm-size 16g \
  -p 8000:8000 \
  vllm-gguf
