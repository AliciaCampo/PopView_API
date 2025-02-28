from fastapi import FastAPI, HTTPException
import mysql.connector
from models import UsuariCreate, Usuari, LlistaCreate, Llista, TitolCreate, Titol
from db import get_db_connection
from typing import List

app = FastAPI()

# ---------------- CRUD USUARI ----------------
@app.post("/usuaris/", response_model=Usuari)
def crear_usuari(usuari: UsuariCreate):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuari (nom, imatge, edat, correu, contrasenya) VALUES (%s, %s, %s, %s, %s)",
                       (usuari.nom, usuari.imatge, usuari.edat, usuari.correu, usuari.contrasenya))
        db.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, **usuari.dict()}
    finally:
        cursor.close()
        db.close()

@app.get("/usuaris/{usuari_id}", response_model=Usuari)
def obtenir_usuari(usuari_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuari WHERE id = %s", (usuari_id,))
        usuari = cursor.fetchone()
        if not usuari:
            raise HTTPException(status_code=404, detail="Usuari no trobat")
        return usuari
    finally:
        cursor.close()
        db.close()

@app.get("/usuaris/", response_model=List[Usuari])
def obtenir_tots_els_usuaris():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuari")
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()

@app.delete("/usuaris/{usuari_id}")
def eliminar_usuari(usuari_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuari WHERE id = %s", (usuari_id,))
        db.commit()
        return {"message": "Usuari eliminat"}
    finally:
        cursor.close()
        db.close()

# ---------------- CRUD LLISTA ----------------
@app.post("/llistes/", response_model=Llista)
def crear_llista(llista: LlistaCreate):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO llista (titol, descripcio, privada, usuari_id) VALUES (%s, %s, %s, %s)",
                       (llista.titol, llista.descripcio, llista.privada, llista.usuari_id))
        db.commit()
        return {"id": cursor.lastrowid, **llista.dict()}
    finally:
        cursor.close()
        db.close()

@app.get("/llistes/{llista_id}", response_model=Llista)
def obtenir_llista(llista_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM llista WHERE id = %s", (llista_id,))
        llista = cursor.fetchone()
        if not llista:
            raise HTTPException(status_code=404, detail="Llista no trobada")
        return llista
    finally:
        cursor.close()
        db.close()

@app.get("/llistes/", response_model=List[Llista])
def obtenir_totes_les_llistes():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM llista")
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()

@app.delete("/llistes/{llista_id}")
def eliminar_llista(llista_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM llista WHERE id = %s", (llista_id,))
        db.commit()
        return {"message": "Llista eliminada"}
    finally:
        cursor.close()
        db.close()

# ---------------- CRUD TITOL ----------------
@app.post("/titols/", response_model=Titol)
def crear_titol(titol: TitolCreate):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO titol (imatge, nom, descripcio, plataformes, rating, comentaris, genero, edadRecomendada) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titol.imatge or None, 
            titol.nom, 
            titol.descripcio or None, 
            titol.plataformes, 
            titol.rating, 
            titol.comentaris or None, 
            titol.genero or None,
            titol.edadRecomendada or None
        ))

        db.commit()
        return {"id": cursor.lastrowid, **titol.dict()}
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# Obtener un título específico por su ID
@app.get("/titols/{titol_id}", response_model=Titol)
def obtenir_titol(titol_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM titol WHERE id = %s", (titol_id,))
        titol = cursor.fetchone()
        if not titol:
            raise HTTPException(status_code=404, detail="Títol no trobat")
        return titol
    finally:
        cursor.close()
        db.close()

@app.get("/titols/", response_model=List[Titol])
def obtenir_tots_els_titols():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM titol")
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()

@app.delete("/titols/{titol_id}")
def eliminar_titol(titol_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM titol WHERE id = %s", (titol_id,))
        db.commit()
        return {"message": "Títol eliminat"}
    finally:
        cursor.close()
        db.close()

# ---------------- RELACIÓ LLISTA-TITOL ----------------
@app.delete("/llistes/{llista_id}/titols/{titol_id}")
def eliminar_titol_de_llista(llista_id: int, titol_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM llista_titols WHERE llista_id = %s AND titol_id = %s", (llista_id, titol_id))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Relació no trobada")
        return {"message": "Títol eliminat de la llista"}
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

