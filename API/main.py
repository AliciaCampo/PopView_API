from fastapi import FastAPI, HTTPException, Depends
import logging
import bcrypt
from mysql.connector import connect, Error
from models import UsuariCreate, Usuari, LlistaCreate, Llista, TitolCreate, Titol
from db import get_db_connection
from typing import List

app = FastAPI()

def get_db():
    """Gestiona automàticament la connexió a la BD amb 'yield'"""
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

# Funció per encriptar contrasenyes
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

#Funció per verificar contrasenyes
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

#CRUD Usuari
@app.post("/usuaris/", response_model=Usuari)
def crear_usuari(usuari: UsuariCreate, db=Depends(get_db)):
    try:
        cursor = db.cursor()

        #Hashejar la contrasenya abans d'emmagatzemar-la
        hashed_password = hash_password(usuari.contrasenya)

        query = """INSERT INTO usuari (nom, imatge, edat, correu, contrasenya) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (usuari.nom, usuari.imatge, usuari.edat, usuari.correu, hashed_password))
        db.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, **usuari.model_dump(exclude={"contrasenya"})}  # No retornem la contrasenya!
    
    except Error as e:
        logging.error(f"Error al crear usuari: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear usuari")
    
    finally:
        cursor.close()

@app.get("/usuaris/{usuari_id}", response_model=Usuari)
def obtenir_usuari(usuari_id: int, db=Depends(get_db)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nom, imatge, edat, correu FROM usuari WHERE id = %s", (usuari_id,))
        usuari = cursor.fetchone()
        if not usuari:
            raise HTTPException(status_code=404, detail="Usuari no trobat")
        return usuari
    except Error as e:
        logging.error(f"Error al obtenir usuari: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtenir usuari")
    finally:
        cursor.close()

@app.get("/usuaris/", response_model=List[Usuari])
def obtenir_tots_els_usuaris(db=Depends(get_db)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nom, imatge, edat, correu FROM usuari")
        return cursor.fetchall()
    except Error as e:
        logging.error(f"Error al obtenir usuaris: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtenir usuaris")
    finally:
        cursor.close()

@app.delete("/usuaris/{usuari_id}")
def eliminar_usuari(usuari_id: int, db=Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuari WHERE id = %s", (usuari_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuari no trobat")
        return {"message": "Usuari eliminat"}
    except Error as e:
        logging.error(f"Error al eliminar usuari: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar usuari")
    finally:
        cursor.close()

#CRUD Llista
@app.post("/llistes/", response_model=Llista)
def crear_llista(llista: LlistaCreate, db=Depends(get_db)):
    try:
        cursor = db.cursor()
        query = "INSERT INTO llista (titol, descripcio, privada) VALUES (%s, %s, %s)"
        cursor.execute(query, (llista.titol, llista.descripcio, llista.privada))
        db.commit()
        return {"id": cursor.lastrowid, **llista.model_dump()}
    except Error as e:
        logging.error(f"Error al crear llista: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear llista")
    finally:
        cursor.close()

#CRUD Títol
@app.post("/titols/", response_model=Titol)
def crear_titol(titol: TitolCreate, db=Depends(get_db)):
    try:
        cursor = db.cursor()
        query = """INSERT INTO titol (imatge, nom, descripcio, plataformes, rating, genero, edadRecomendada) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (
            titol.imatge, titol.nom, titol.descripcio, 
            titol.plataformes, titol.rating, titol.genero, titol.edadRecomendada
        ))
        db.commit()
        return {"id": cursor.lastrowid, **titol.model_dump()}
    except Error as e:
        logging.error(f"Error al crear títol: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear títol")
    finally:
        cursor.close()

#DELETE Títol de Llista
@app.delete("/llistes/{llista_id}/titols/{titol_id}")
def eliminar_titol_de_llista(llista_id: int, titol_id: int, db=Depends(get_db)):
    try:
        cursor = db.cursor()
        query = "DELETE FROM llista_titols WHERE llista_id = %s AND titol_id = %s"
        cursor.execute(query, (llista_id, titol_id))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Relació no trobada entre la llista i el títol")
        return {"message": "Títol eliminat de la llista"}
    except Error as e:
        logging.error(f"Error al eliminar títol de la llista: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar títol de la llista")
    finally:
        cursor.close()
