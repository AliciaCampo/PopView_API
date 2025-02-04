from fastapi import FastAPI, HTTPException
import mysql.connector
from models import UsuariCreate, Usuari, LlistaCreate, Llista, TitolCreate, Titol
from database import get_db_connection

app = FastAPI()

# CRUD Usuari
@app.post("/usuaris/", response_model=Usuari)
def crear_usuari(usuari: UsuariCreate):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO usuari (nom, imatge, edat, correu, contrasenya) VALUES (%s, %s, %s, %s, %s)",
                   (usuari.nom, usuari.imatge, usuari.edat, usuari.correu, usuari.contrasenya))
    db.commit()
    user_id = cursor.lastrowid
    cursor.close()
    db.close()
    return {"id": user_id, **usuari.dict()}

@app.get("/usuaris/{usuari_id}", response_model=Usuari)
def obtenir_usuari(usuari_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuari WHERE id = %s", (usuari_id,))
    usuari = cursor.fetchone()
    cursor.close()
    db.close()
    if usuari is None:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return usuari

@app.delete("/usuaris/{usuari_id}")
def eliminar_usuari(usuari_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuari WHERE id = %s", (usuari_id,))
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Usuari eliminat"}

# CRUD Llista
@app.post("/llistes/", response_model=Llista)
def crear_llista(llista: LlistaCreate):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO llista (titol, descripcio, privada) VALUES (%s, %s, %s)",
                   (llista.titol, llista.descripcio, llista.privada))
    db.commit()
    llista_id = cursor.lastrowid
    cursor.close()
    db.close()
    return {"id": llista_id, **llista.dict()}

@app.get("/llistes/{llista_id}", response_model=Llista)
def obtenir_llista(llista_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM llista WHERE id = %s", (llista_id,))
    llista = cursor.fetchone()
    cursor.close()
    db.close()
    if llista is None:
        raise HTTPException(status_code=404, detail="Llista no trobada")
    return llista

# CRUD Titol
@app.post("/titols/", response_model=Titol)
def crear_titol(titol: TitolCreate):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO titol (imatge, nom, descripcio, plataformes, es_peli, rating, comentaris) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (titol.imatge, titol.nom, titol.descripcio, titol.plataformes, titol.es_peli, titol.rating, titol.comentaris))
    db.commit()
    titol_id = cursor.lastrowid
    cursor.close()
    db.close()
    return {"id": titol_id, **titol.dict()}

@app.get("/titols/{titol_id}", response_model=Titol)
def obtenir_titol(titol_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM titol WHERE id = %s", (titol_id,))
    titol = cursor.fetchone()
    cursor.close()
    db.close()
    if titol is None:
        raise HTTPException(status_code=404, detail="Títol no trobat")
    return titol
