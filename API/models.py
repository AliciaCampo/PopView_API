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
class Llista(BaseModel):
    titol: str
    descripcio: Optional[str] = None
    privada: bool
    titols: List[int] = []
class LlistaCreate(BaseModel):
    titol: str
    descripcio: Optional[str] = None
    privada: bool  # No incluye `titols` al momento de crear
class Titol(BaseModel):
    imatge: Optional[str] = None
    nom: str
    descripcio: Optional[str] = None
    plataformes: str
    es_peli: bool
    rating: float
    comentaris: Optional[str] = None
class TitolCreate(BaseModel):
    imatge: Optional[str] = None
    nom: str
    descripcio: Optional[str] = None
    plataformes: str
    es_peli: bool
    rating: float