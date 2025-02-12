from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class Usuari(BaseModel):
    nom: str
    imatge: Optional[str] = None
    edat: int
    correu: str
    contrasenya: str
    llistes: List[int] = []

class Llista(BaseModel):
    titol: str
    descripcio: Optional[str] = None
    privada: bool
    titols: List[int] = []

class Titol(BaseModel):
    imatge: Optional[str] = None
    nom: str
    descripcio: Optional[str] = None
    plataformes: str
    es_peli: bool
    rating: float
    comentaris: Optional[str] = None
