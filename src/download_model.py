import os
from huggingface_hub import hf_hub_download


def download_model():
    # Replace these with your model details
    repo_id = "lumolabs-ai/Lumo-8B-Instruct"
    filename = "Lumo-8B-Instruct-FT-Q4_0.gguf"

    local_path = hf_hub_download(
        repo_id=repo_id, filename=filename, local_dir="/models"
    )
    print(f"Model downloaded to: {local_path}")
    return local_path


if __name__ == "__main__":
    download_model()
