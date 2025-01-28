# Dockerfile
FROM vllm/vllm-openai:v0.7.0

# Install git and git-lfs for downloading models
RUN apt-get update && \
    apt-get install -y git git-lfs && \
    git lfs install

# Create directories
RUN mkdir -p /models

# Download script
COPY download_model.py /download_model.py
COPY start.sh /start.sh
RUN chmod +x /start.sh


ENTRYPOINT ["/bin/sh"]
CMD ["/start.sh"]
