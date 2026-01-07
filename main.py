from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
from services.ai_service import AIService
import shutil
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
ai = AIService()

# Creamos una carpeta temporal para los audios
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/status")
def status():
    return ai.obtener_info_hardware()

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    ruta_archivo = os.path.join(UPLOAD_DIR, file.filename)
    
    # Guardar el archivo en el disco
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Procesar con whisper
    resultado = ai.transcribir_audio(ruta_archivo)
    
    return {
        "filename": file.filename,
        "transcripcion": resultado
    }
