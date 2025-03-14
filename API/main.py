from fastapi import FastAPI, HTTPException
import mysql.connector
from models import UsuariCreate, Usuari, UsuariUpdate, LlistaCreate, Llista, LlistaUpdate, TitolCreate, Titol, ComentarioCreate, ComentarioUpdate, RatingUpdate
from db import get_db_connection
from typing import List

app = FastAPI()

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
            titol.genero or None,
            titol.edadRecomendada or None
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
        if titol is None:
            raise HTTPException(status_code=404, detail="Título no encontrado")
        return titol
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el título: {str(e)}")
    finally:
        cursor.close()
        db.close()

@app.get("/titols/", response_model=List[Titol])
def obtenir_tots_els_titols():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM titol")
        titols = cursor.fetchall()
        return titols
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los títulos: {str(e)}")
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
@app.delete("/llistes/{llista_id}/titols/{titol_id}")
def eliminar_titol_de_llista(llista_id: int, titol_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Usar el nombre correcto de la tabla: llista_titol
        cursor.execute("DELETE FROM llista_titol WHERE llista_id = %s AND titol_id = %s", (llista_id, titol_id))
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


# CRUD Llista
@app.post("/llistes/", response_model=Llista)
def crear_llista(llista: LlistaCreate):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Verificar que el usuario existe
        cursor.execute("SELECT * FROM usuari WHERE id = %s", (llista.usuari_id,))
        usuari = cursor.fetchone()

        if not usuari:
            raise HTTPException(status_code=404, detail="Usuari no trobat")
        
        # Crear la lista (QUITAMOS usuari_id de la inserción)
        cursor.execute("""
            INSERT INTO llista (titol, descripcio, privada) 
            VALUES (%s, %s, %s)
        """, (llista.titol, llista.descripcio, llista.privada))
        db.commit()
        llista_id = cursor.lastrowid

        # Insertar en la tabla intermedia para vincular usuario y lista
        cursor.execute("""
            INSERT INTO usuari_llista (usuari_id, llista_id)
            VALUES (%s, %s)
        """, (llista.usuari_id, llista_id))
        db.commit()

        return {"id": llista_id, **llista.dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear llista: {str(e)}")
    
    finally:
        cursor.close()
        db.close()

@app.post("/llistes/{llista_id}/titols/{titol_id}", response_model=dict)
def afegir_titol_a_llista(llista_id: int, titol_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Verificar si la lista y el título existen
        cursor.execute("SELECT * FROM llista WHERE id = %s", (llista_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Llista no trobada")
        cursor.execute("SELECT * FROM titol WHERE id = %s", (titol_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Títol no trobat")
        # Verificar si el título ya está en la lista
        cursor.execute("SELECT * FROM llista_titol WHERE llista_id = %s AND titol_id = %s", (llista_id, titol_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El títol ja està en la llista")
        # Insertar el título en la lista
        cursor.execute("INSERT INTO llista_titol (llista_id, titol_id) VALUES (%s, %s)", (llista_id, titol_id))
        db.commit()
        return {"message": "Títol afegit a la llista correctament"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al afegir títol a la llista: {str(e)}")
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
@app.get("/llistes/publicas/", response_model=List[Llista])
def obtenir_llistes_publicas():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        # Filtrar las listas donde el campo `privada` es False
        cursor.execute("SELECT * FROM llista WHERE privada = FALSE")
        llistes = cursor.fetchall()
        return llistes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener listas públicas: {str(e)}")
    finally:
        cursor.close()
        db.close()

@app.get("/usuaris/{usuari_id}/llistes", response_model=List[Llista])
def obtenir_llistes_per_usuari(usuari_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.*
            FROM llista l
            JOIN usuari_llista ul ON l.id = ul.llista_id
            WHERE ul.usuari_id = %s
        """, (usuari_id,))
        llistes = cursor.fetchall()
        if not llistes:
            raise HTTPException(status_code=404, detail="No s'han trobat llistes per aquest usuari")
        return llistes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir llistes per usuari: {str(e)}")
    finally:
        cursor.close()
        db.close()

@app.get("/llistes/{llista_id}/titols", response_model=List[Titol])
def obtenir_titols_de_llista(llista_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*
            FROM titol t
            JOIN llista_titol lt ON t.id = lt.titol_id
            WHERE lt.llista_id = %s
        """, (llista_id,))
        titols = cursor.fetchall()
        if not titols:
            raise HTTPException(status_code=404, detail="No s'han trobat títols per aquesta llista")
        return titols
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir els títols de la llista: {str(e)}")
    finally:
        cursor.close()
        db.close()

@app.put("/llistes/{llista_id}", response_model=Llista)
def actualizar_llista(llista_id: int, llista_update: LlistaUpdate):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        fields = []
        values = []
        if llista_update.titol is not None:
            fields.append("titol = %s")
            values.append(llista_update.titol)
        if llista_update.descripcio is not None:
            fields.append("descripcio = %s")
            values.append(llista_update.descripcio)
        if llista_update.privada is not None:
            fields.append("privada = %s")
            values.append(llista_update.privada)
        if not fields:
            raise HTTPException(status_code=400, detail="No hi ha camps per actualitzar")
        values.append(llista_id)
        query = f"UPDATE llista SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, tuple(values))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Llista no trobada")
        cursor.execute("SELECT * FROM llista WHERE id = %s", (llista_id,))
        llista_actualizada = cursor.fetchone()
        return llista_actualizada
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar llista: {str(e)}")
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

        if usuari_update.correu is not None:
            fields.append("correu = %s")
            values.append(usuari_update.correu)

        if usuari_update.contrasenya is not None:
            fields.append("contrasenya = %s")
            values.append(usuari_update.contrasenya)
        if not fields:
            raise HTTPException(status_code=400, detail="No hi ha camps per actualitzar")
        values.append(usuari_id)
        query = f"UPDATE usuari SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, tuple(values))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuari no trobat")
        # Retornar el usuario actualizado
        cursor.execute("SELECT * FROM usuari WHERE id = %s", (usuari_id,))
        usuari_actualitzat = cursor.fetchone()
        return usuari_actualitzat
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuari: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
@app.post("/usuaris/{usuari_id}/titols/{titol_id}/comentarios/")
def agregar_comentario(usuari_id: int, titol_id: int, comentario: ComentarioCreate):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO usuari_titol (usuari_id, titol_id, comentaris, rating)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE comentaris = VALUES(comentaris), rating = VALUES(rating)
        """, (usuari_id, titol_id, comentario.comentario, comentario.rating))
        db.commit()
        return {"message": "Comentario y valoración añadidos"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al añadir comentario: {str(e)}")
    finally:
        cursor.close()
        db.close()
@app.get("/usuaris/{usuari_id}/titols/{titol_id}/comentarios/")
def obtener_comentarios(usuari_id: int, titol_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT comentaris, rating
            FROM usuari_titol
            WHERE usuari_id = %s AND titol_id = %s
        """, (usuari_id, titol_id))
        comentarios = cursor.fetchall()
        if not comentarios:
            raise HTTPException(status_code=404, detail="Comentarios no encontrados")
        return comentarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener comentarios: {str(e)}")
    finally:
        cursor.close()
        db.close()
@app.get("/titols/{titol_id}/comentarios/")
def obtener_todos_los_comentarios(titol_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT usuari_id, comentaris, rating
            FROM usuari_titol
            WHERE titol_id = %s AND comentaris IS NOT NULL
        """, (titol_id,))
        comentarios = cursor.fetchall()
        if not comentarios:
            raise HTTPException(status_code=404, detail="No hay comentarios para este título")
        return comentarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener comentarios: {str(e)}")
    finally:
        cursor.close()
        db.close()
@app.put("/usuaris/{usuari_id}/titols/{titol_id}/comentarios/")
def modificar_comentario(usuari_id: int, titol_id: int, comentario: ComentarioUpdate):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        fields = []
        values = []
        if comentario.comentario is not None:
            fields.append("comentaris = %s")
            values.append(comentario.comentario)
        if comentario.rating is not None:
            fields.append("rating = %s")
            values.append(comentario.rating)
        if not fields:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        values.append(usuari_id)
        values.append(titol_id)
        query = f"UPDATE usuari_titol SET {', '.join(fields)} WHERE usuari_id = %s AND titol_id = %s"
        cursor.execute(query, tuple(values))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        return {"message": "Comentario y valoración modificados"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al modificar comentario: {str(e)}")
    finally:
        cursor.close()
        db.close()

@app.delete("/usuaris/{usuari_id}/titols/{titol_id}/comentarios/")
def eliminar_comentario(usuari_id: int, titol_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE usuari_titol
            SET comentaris = NULL, rating = 0
            WHERE usuari_id = %s AND titol_id = %s
        """, (usuari_id, titol_id))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        return {"message": "Comentario eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar comentario: {str(e)}")
    finally:
        cursor.close()
        db.close()

@app.put("/usuaris/{usuari_id}/titols/{titol_id}/rating/")
def actualizar_rating(usuari_id: int, titol_id: int, rating_update: RatingUpdate):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Verificar que el rating esté en el rango permitido
        if rating_update.rating not in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]:
            raise HTTPException(status_code=400, detail="El rating debe estar entre 0 y 4 con incrementos de 0.5")

        cursor.execute("""
            UPDATE usuari_titol
            SET rating = %s
            WHERE usuari_id = %s AND titol_id = %s
        """, (rating_update.rating, usuari_id, titol_id))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Rating no encontrado")

        return {"message": "Rating actualizado"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar rating: {str(e)}")
    finally:
        cursor.close()
        db.close()
