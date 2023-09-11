import transformers
from huggingface_hub import snapshot_download
import os

MODEL_NAME = os.environ.get("MODEL_NAME")

# Ensure directory exists before downloading
os.makedirs("/model", exist_ok=True)
# Ensure directory is empty before downloading
for file in os.listdir("/model"):
    os.remove(os.path.join("/model", file))

snapshot_download(MODEL_NAME, local_dir="/model")
transformers.utils.move_cache()