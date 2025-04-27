from flask import Flask, render_template, jsonify, request
from config import Config, flask_app_config
import json
import os

from apscheduler.schedulers.background import BackgroundScheduler

def rotazione_turni():
    print("avvio rotazione turni")
    turni = carica_turni()
    print(turni)

    # Impostiamo tutti i turni come non completati prima di ruotarli
    for turno in turni:
        turno['completato'] = False

    # Estraiamo i compiti
    compiti = [turno['compito'] for turno in turni]

    # Ruotiamo i compiti (compreso "Riposo")
    compiti = compiti[1:] + [compiti[0]]  # Ruotiamo la lista dei compiti

    # Riassegniamo i compiti alle persone (i nomi rimangono fermi)
    for i, turno in enumerate(turni):
        turno['compito'] = compiti[i]
        
    print("avvio rotazione turni")

    salva_turni(turni)
    
    print(turni)

# Configurazione di APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(rotazione_turni, 'interval', minutes=2)
scheduler.start()

# Inizializza Flask
app = Flask(__name__)
app.config.from_object(Config)

# Path del file JSON per salvare i dati dei turni
DATA_FILE = "turni.json"

# Dati di esempio iniziali
DEFAULT_TURNI = [
    {"nome": "Raffaello", "compito": "Bagno Cacca", "completato": False},
    {"nome": "Ettore", "compito": "Cucina", "completato": False},
    {"nome": "Pierclaudio", "compito": "Riposo", "completato": False},
    {"nome": "Francesco", "compito": "Bagno Doccia", "completato": False}
]

# Funzione per caricare i turni dal file
def carica_turni():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return DEFAULT_TURNI

# Funzione per salvare i turni nel file
def salva_turni(turni):
    with open(DATA_FILE, "w") as file:
        json.dump(turni, file)

@app.route("/")
def index():
    turni = carica_turni()
    return render_template("index.html", turni=turni)

@app.route("/completa", methods=["POST"])
def completa_turno():
    data = request.json
    turno_index = data.get("index")
    turni = carica_turni()

    if turno_index is not None and 0 <= turno_index < len(turni):
        turni[turno_index]["completato"] = True
        salva_turni(turni)
        return jsonify({"success": True})
    
    return jsonify({"success": False}), 400


@app.route("/rotazione", methods=["POST"])
def rotazione_manuale():
    rotazione_turni()
    return jsonify({"success": True})

@app.route("/stato_turni", methods=["GET"])
def stato_turni():
    turni = carica_turni()  # Carica i turni dal file
    return jsonify(turni)  # Restituisce i turni come JSON


if __name__ == "__main__":
    app.run(**flask_app_config)
