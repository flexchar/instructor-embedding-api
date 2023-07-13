from huggingface_hub import snapshot_download
import os

MODEL_NAME = os.environ.get("MODEL_NAME")

snapshot_download(MODEL_NAME)