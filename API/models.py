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
    id: int
    titol: str
    descripcio: Optional[str] = None
    privada: bool
    titols: List[int] = []
class LlistaCreate(BaseModel):
    titol: str
    descripcio: Optional[str] = None
    privada: bool  # No incluye `titols` al momento de crear
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
class TitolCreate(BaseModel):
    imatge: Optional[str] = None
    nom: str
    descripcio: Optional[str] = None
    plataformes: str
    rating: float
    comentaris: Optional[str] = None
    genero: Optional[str] = None
    edadRecomendada: Optional[int] = None