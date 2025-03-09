from fastapi import FastAPI, HTTPException
import mysql.connector
from models import UsuariCreate, Usuari, UsuariUpdate, LlistaCreate, Llista, TitolCreate, Titol
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
        return {"id": user_id, **usuari.model_dump()}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de dades: {err}")
    finally:
        if cursor:
            cursor.close()
        if db:
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
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de dades: {err}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.delete("/usuaris/{usuari_id}")
def eliminar_usuari(usuari_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuari WHERE id = %s", (usuari_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuari no trobat")
        return {"message": "Usuari eliminat"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de dades: {err}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.put("/usuaris/{usuari_id}")
def actualitzar_usuari(usuari_id: int, usuari_update: UsuariUpdate):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        fields = []
        values = []

        if usuari_update.nom is not None:
            fields.append("nom = %s")
            values.append(usuari_update.nom)

        if usuari_update.imatge is not None:
            fields.append("imatge = %s")
            values.append(usuari_update.imatge)

        if usuari_update.edat is not None:
            fields.append("edat = %s")
            values.append(usuari_update.edat)

        if not fields:
            raise HTTPException(status_code=400, detail="No hi ha camps per actualitzar")

        values.append(usuari_id)
        query = f"UPDATE usuari SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, tuple(values))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuari no trobat")

        return {"message": "Usuari actualitzat correctament"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de dades: {err}")
    finally:
        if cursor:
            cursor.close()
        if db:
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
        return {"id": cursor.lastrowid, **llista.model_dump()}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de dades: {err}")
    finally:
        if cursor:
            cursor.close()
        if db:
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
        return {"id": cursor.lastrowid, **titol.model_dump()}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de dades: {err}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

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
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de dades: {err}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
