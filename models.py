from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class usuario(BaseModel):
    id: str = Field(..., example='u1')
    nombre: str = Field(..., example='Daniel')
    email: EmailStr = Field(..., example='daniel.calle@teamsoft.com')
    edad: int = Field(..., example=40)

class proyecto(BaseModel):
    id: str = Field(..., example='p1')
    nombre: str = Field(..., example='proyecto1')
    descripcion: Optional[str] = Field(None, example='Primer proyecto de construccion de app1')
    id_usuario: str = Field(..., example='u1')
    fecha_creacion: datetime = Field(..., example='2024-10-31T19:00:00Z')
