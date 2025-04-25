
from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

dimensione_file = "dimensione.xlsx"
disponibile_file = "disponibile.xlsx"

def carica_dati():
    if os.path.exists(dimensione_file):
        df_dimensione = pd.read_excel(dimensione_file, engine="openpyxl")
    else:
        df_dimensione = pd.DataFrame(columns=["risorsa", "dimensione"])
    
    if os.path.exists(disponibile_file):
        df_disponibile = pd.read_excel(disponibile_file, engine="openpyxl")
    else:
        df_disponibile = pd.DataFrame(columns=["risorsa", "disponibile"])
    
    today = datetime.now().strftime("%d/%m/%y")
    df = pd.merge(df_dimensione, df_disponibile, on="risorsa", how="left")
    df["disponibile"].fillna(today, inplace=True)
    return df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_dimensione", methods=["POST"])
def upload_dimensione():
    file = request.files["file"]
    file.save(dimensione_file)
    return jsonify({"message": "File dimensione caricato!"})

@app.route("/upload_disponibile", methods=["POST"])
def upload_disponibile():
    file = request.files["file"]
    file.save(disponibile_file)
    return jsonify({"message": "File disponibilità caricato!"})

@app.route("/search")
def search():
    dimensione = request.args.get("dimensione", type=float)
    disponibile = request.args.get("disponibile")

    df = carica_dati()

    results = []
    for _, row in df.iterrows():
        dim = float(row["dimensione"])
        disp = row["disponibile"]
        disp_date = datetime.strptime(disp, "%d/%m/%y")
        filtro_date = datetime.strptime(disponibile, "%d/%m/%y")

        if (not dimensione or dim >= dimensione) and (not disponibile or disp_date >= filtro_date):
            results.append({
                "risorsa": str(row["risorsa"]).zfill(4),
                "dimensione": f"{row['dimensione']:.2f}",
                "disponibile": row["disponibile"]
            })

    results = sorted(results, key=lambda x: (datetime.strptime(x["disponibile"], "%d/%m/%y"),
                                              float(x["dimensione"]), x["risorsa"]))

    return jsonify(success=True, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
