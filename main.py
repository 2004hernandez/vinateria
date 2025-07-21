from fastapi import FastAPI, Query
import joblib
import os
import random

# Cargar modelo
modelo_path = os.path.join(os.path.dirname(__file__), "vinateria.pkl")
rules = joblib.load(modelo_path)

app = FastAPI()

def recomendar_ids(ids, limite=15):
    ids_input = set(f"curado_{i}" for i in ids)
    recomendados = set()

    for _, fila in rules.iterrows():
        if ids_input == fila['antecedents']:
            for conseq in fila['consequents']:
                try:
                    id_recom = int(conseq.replace("curado_", ""))
                    if id_recom not in ids:
                        recomendados.add(id_recom)
                except:
                    continue

    recomendados = list(recomendados)

    # Usar semilla basada en IDs de entrada para que sea determinista
    semilla = sum(ids)  # cualquier función hash simple que sea reproducible
    random.seed(semilla)
    random.shuffle(recomendados)

    return sorted(recomendados[:limite])

@app.get("/recomendar")
def obtener_recomendaciones(ids: list[int] = Query(...)):
    return {
        "input_ids": ids,
        "ids_recomendados": recomendar_ids(ids)
    }
