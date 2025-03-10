from pydantic import BaseModel
from typing import Optional
from typing import Optional, List
from datetime import date

class Usuari(BaseModel):
    id: int
    nom: str
    imatge: Optional[str] = None
    edat: int
    correu: str
    contrasenya: str
    llistes: List[int] = []
class UsuariCreate(BaseModel):
    nom: str
    imatge: Optional[str] = None
    edat: int
    correu: str
    contrasenya: str 
class UsuariUpdate(BaseModel):
    nom: Optional[str] = None
    imatge: Optional[str] = None
    edat: Optional[int] = None
    correu: Optional[str] = None
    contrasenya: Optional[str] = None
class Llista(BaseModel):
    id: int
    titol: str
    descripcio: Optional[str] = None
    privada: bool
    titols: List[int] = []
class LlistaUpdate(BaseModel):
    titol: Optional[str] = None
    descripcio: Optional[str] = None
    privada: Optional[bool] = None
class LlistaCreate(BaseModel):
    titol: str
    descripcio: Optional[str] = None
    privada: bool  # No incluye `titols` al momento de crear
    usuari_id: int
class Titol(BaseModel):
    id: int
    imatge: Optional[str] = None
    nom: str
    descripcio: Optional[str] = None
    plataformes: str
    rating: float
    comentaris: Optional[str] = None
    genero: Optional[str] = None
    edadRecomendada: Optional[int] = None

    class Config:
        orm_mode = True  # Permite trabajar con los objetos de SQLAlchemy o consultas directas
class TitolCreate(BaseModel):
    imatge: Optional[str] = None
    nom: str
    descripcio: Optional[str] = None
    plataformes: str
    rating: float
    comentaris: Optional[str] = None
    genero: Optional[str] = None
    edadRecomendada: Optional[int] = None
