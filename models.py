from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base

class Grabacion(Base):
    __tablename__ = "grabaciones"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    texto_transcrito = Column(Text)
    idioma = Column(String)
    duracion_proceso = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.now)