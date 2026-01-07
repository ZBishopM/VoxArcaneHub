from fastapi import FastAPI
import torch

app = FastAPI()

@app.get("/")
def status():
    return {
        "sistema": "VoxArcane API",
        "gpu_detectada": torch.cuda.is_available(),
        "gpu_nombre": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Ninguna"
    }