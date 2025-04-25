
from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

dimensione_data = {}
disponibile_data = {}

def carica_dimensione(path):
    df = pd.read_excel(path)
    return {str(row['risorsa']).zfill(4): float(row['dimensione']) for _, row in df.iterrows()}

def carica_disponibile(path):
    df = pd.read_excel(path)
    return {
        str(row['risorsa']).zfill(4): datetime.strptime(str(row['disponibile']), "%d/%m/%y").strftime("%d/%m/%y")
        if not pd.isna(row['disponibile']) else datetime.now().strftime("%d/%m/%y")
        for _, row in df.iterrows()
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_dimensione", methods=["POST"])
def upload_dimensione():
    f = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, "dimensione.xlsx")
    f.save(path)
    global dimensione_data
    dimensione_data = carica_dimensione(path)
    return jsonify({"success": True, "message": "File dimensione caricato."})

@app.route("/upload_disponibile", methods=["POST"])
def upload_disponibile():
    f = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, "disponibile.xlsx")
    f.save(path)
    global disponibile_data
    disponibile_data = carica_disponibile(path)
    return jsonify({"success": True, "message": "File disponibile caricato."})

@app.route("/search")
def search():
    min_d = request.args.get("dimensione", type=float)
    disponibile_filtro = request.args.get("disponibile")

    results = []
    for risorsa, dim in dimensione_data.items():
        disp = disponibile_data.get(risorsa, datetime.now().strftime("%d/%m/%y"))
        if (not min_d or dim >= min_d):
            disp_date = datetime.strptime(disp, "%d/%m/%y")
            filtro_date = datetime.strptime(disponibile_filtro, "%d/%m/%y")
            if disp_date >= filtro_date:
                results.append({
                    "risorsa": risorsa,
                    "dimensione": f"{dim:.2f}",
                    "disponibile": disp
                })
    results.sort(key=lambda x: (x["disponibile"], float(x["dimensione"]), x["risorsa"]))
    return jsonify({"success": True, "results": results})
