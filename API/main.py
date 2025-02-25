from fastapi import FastAPI, HTTPException
import mysql.connector
from models import UsuariCreate, Usuari, LlistaCreate, Llista, TitolCreate, Titol
from db import get_db_connection
from typing import List

app = FastAPI()

# CRUD Usuari
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuari: {str(e)}")
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
        if usuari is None:
            raise HTTPException(status_code=404, detail="Usuari no trobat")
        return usuari
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir usuari: {str(e)}")
    finally:
        cursor.close()
        db.close()

@app.get("/usuaris/", response_model=List[Usuari])
def obtenir_tots_els_usuaris():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuari")
        usuaris = cursor.fetchall()
        return usuaris
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir usuaris: {str(e)}")
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuari: {str(e)}")
    finally:
        cursor.close()
        db.close()

# CRUD Llista
@app.post("/llistes/", response_model=Llista)
def crear_llista(llista: LlistaCreate):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO llista (titol, descripcio, privada) VALUES (%s, %s, %s)",
                       (llista.titol, llista.descripcio, llista.privada))
        db.commit()
        llista_id = cursor.lastrowid
        return {"id": llista_id, **llista.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear llista: {str(e)}")
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
        if llista is None:
            raise HTTPException(status_code=404, detail="Llista no trobada")
        return llista
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir llista: {str(e)}")
    finally:
        cursor.close()
        db.close()

@app.get("/llistes/", response_model=List[Llista])
def obtenir_totes_les_llistes():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM llista")
        llistes = cursor.fetchall()
        return llistes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir llistes: {str(e)}")
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar llista: {str(e)}")
    finally:
        cursor.close()
        db.close()

# CRUD Titol
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir títol: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.get("/titols/", response_model=List[Titol])
def obtenir_tots_els_titols():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM titol")
        titols = cursor.fetchall()

        if not titols:
            return []

        return titols
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir títols: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.delete("/titols/{titol_id}")
def eliminar_titol(titol_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM titol WHERE id = %s", (titol_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Títol no trobat")

        return {"message": "Títol eliminat correctament"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar títol: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

