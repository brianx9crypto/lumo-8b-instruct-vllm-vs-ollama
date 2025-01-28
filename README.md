# Lumo 8B Instruct Optimization

- Optimizated configuration for Lumo 8B Instruct model with 1.5x to 3x speed gains.
- Benchmark on AWS G6e.2xLarge (Nvidia L40S)

### Results -

1. Ollama benchmark
   ![Ollama benchmark](./bench/Ollama%20Bench.jpeg)
2. vLLM benchmark
   ![vLLM benchmark](./bench/vLLM%20Bench.jpeg)

### How to setup?

- Get nvidia L40S or above GPU instance
- Ubuntu VM preferred
  - Install [Docker](https://docs.docker.com/engine/install/ubuntu/), nVidia-cuda drivers, [nvidia tool kit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- Install [Ollama](https://ollama.com/download/linux) (optional; for comparison or to reproduce these tests)

```bash
cd src
# Build vLLM docker image and run
./run.sh
# OR manual mode
docker build . -t vllm-gguf

# Run the container
docker run --gpus all \
  --shm-size 16g \
  -p 8000:8000 \
  vllm-gguf
```

- Benchmark
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/test_model.py
```

### Roadmap -

- [ ] More optimizations to Docker image
- [ ] Image on Docker hub
- [ ] Serverless configuration
