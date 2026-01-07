from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil
import os
import time

from services.ai_service import AIService
from database import engine, Base, get_db
from models import Grabacion

# Crear tablas automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI()
ai = AIService()

app.mount("/static", StaticFiles(directory="static"), name="static")
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/status")
def status():
    return ai.obtener_info_hardware()

@app.get("/historial")
def obtener_historial(db: Session = Depends(get_db)):
    return db.query(Grabacion).order_by(Grabacion.id.desc()).all()
    

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ruta_archivo = os.path.join(UPLOAD_DIR, file.filename)
    
    # 1. Guardar temporalmente
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Medir tiempo y Whisper
    inicio = time.time()
    resultado = ai.transcribir_audio(ruta_archivo)
    fin = time.time()
    tiempo_total = f"{fin - inicio:.2f} seg"
    
    # 3. Guardar
    nueva_grabacion = Grabacion(
        filename=file.filename,
        texto_transcrito=resultado["texto"],
        idioma=resultado["idioma"],
        duracion_proceso=tiempo_total
    )
    db.add(nueva_grabacion)
    db.commit()
    db.refresh(nueva_grabacion) # Recuperar el ID generado
    
    return {
        "id": nueva_grabacion.id,
        "filename": nueva_grabacion.filename,
        "transcripcion": resultado,
        "tiempo_procesamiento": tiempo_total
    }