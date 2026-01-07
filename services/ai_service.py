import torch
import whisper
import os

class AIService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model("base", device=self.device)

    def transcribir_audio(self, ruta_archivo: str):
        if not os.path.exists(ruta_archivo):
            return {"error": "Archivo no encontrado"}
        
        resultado = self.model.transcribe(ruta_archivo)
        return {
            "texto": resultado["text"],
            "idioma": resultado["language"]
        }

    def obtener_info_hardware(self):
        return {
            "dispositivo": self.device,
            "modelo": torch.cuda.get_device_name(0) if self.device == "cuda" else "CPU",
            "vram_libre": f"{torch.cuda.mem_get_info()[0] // 1024**2} MB"
        }