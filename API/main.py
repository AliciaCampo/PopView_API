from fastapi import FastAPI, HTTPException
import mysql.connector
from models import UsuariCreate, Usuari, LlistaCreate, Llista, TitolCreate, Titol
from db import get_db_connection
from typing import List, Optional

app = FastAPI()

# CRUD Usuari
@app.post("/usuaris/", response_model=Usuari)
def crear_usuari(usuari: UsuariCreate):
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuari (nom, imatge, edat, correu, contrasenya) VALUES (%s, %s, %s, %s, %s)",
                       (usuari.nom, usuari.imatge or None, usuari.edat, usuari.correu, usuari.contrasenya))
        db.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, **usuari.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuari: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.get("/usuaris/{usuari_id}", response_model=Usuari)
def obtenir_usuari(usuari_id: int):
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuari WHERE id = %s", (usuari_id,))
        usuari = cursor.fetchone()
        if usuari is None:
            raise HTTPException(status_code=404, detail="Usuari no trobat")
        return usuari
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir usuari: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.delete("/usuaris/{usuari_id}")
def eliminar_usuari(usuari_id: int):
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuari WHERE id = %s", (usuari_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuari no trobat")
        return {"message": "Usuari eliminat"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuari: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# CRUD Llista
@app.post("/llistes/", response_model=Llista)
def crear_llista(llista: LlistaCreate):
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO llista (titol, descripcio, privada) VALUES (%s, %s, %s)",
                       (llista.titol, llista.descripcio or None, llista.privada))
        db.commit()
        llista_id = cursor.lastrowid
        return {"id": llista_id, **llista.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear llista: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.delete("/llistes/{llista_id}")
def eliminar_llista(llista_id: int):
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM llista WHERE id = %s", (llista_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Llista no trobada")
        return {"message": "Llista eliminada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar llista: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# CRUD Titol
@app.post("/titols/", response_model=Titol)
def crear_titol(titol: TitolCreate):
    db = None
    cursor = None
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
            titol.genero, 
            titol.edadRecomendada
        ))
        db.commit()
        titol_id = cursor.lastrowid
        return {"id": titol_id, **titol.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear títol: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.delete("/titols/{titol_id}")
def eliminar_titol(titol_id: int):
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM titol WHERE id = %s", (titol_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Títol no trobat")
        return {"message": "Títol eliminat"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar títol: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.delete("/llistes/{llista_id}/titols/{titol_id}")
def eliminar_titol_de_llista(llista_id: int, titol_id: int):
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM llista_titols WHERE llista_id = %s AND titol_id = %s", (llista_id, titol_id))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Relació no trobada entre la llista i el títol")
        return {"message": "Títol eliminat de la llista"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar títol de la llista: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
