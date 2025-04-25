
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

disponibile_path = os.path.join(UPLOAD_FOLDER, 'disponibile.xlsx')
dimensione_path = os.path.join(UPLOAD_FOLDER, 'dimensione.xlsx')

# Carica disponibile all'avvio se esiste
df_disponibile = None
if os.path.exists(disponibile_path):
    try:
        df_disponibile = pd.read_excel(disponibile_path, dtype=str)
    except Exception:
        df_disponibile = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload_disponibile', methods=['POST'])
def upload_disponibile():
    global df_disponibile
    file = request.files.get('file')
    if not file:
        return jsonify(success=False, message="File non ricevuto.")
    try:
        file.save(disponibile_path)
        df_disponibile = pd.read_excel(disponibile_path, dtype=str)
        return jsonify(success=True, message="File 'disponibile.xlsx' caricato correttamente.")
    except Exception as e:
        return jsonify(success=False, message=f"Errore nel caricamento: {str(e)}")

@app.route('/upload_dimensione', methods=['POST'])
def upload_dimensione():
    file = request.files.get('file')
    if not file:
        return jsonify(success=False, message="File non ricevuto.")
    try:
        file.save(dimensione_path)
        return jsonify(success=True, message="File 'dimensione.xlsx' aggiornato correttamente.")
    except Exception as e:
        return jsonify(success=False, message=f"Errore nel caricamento: {str(e)}")

@app.route('/cerca', methods=['POST'])
def cerca():
    if not os.path.exists(dimensione_path) or df_disponibile is None:
        return jsonify([])

    try:
        df_dimensione = pd.read_excel(dimensione_path, dtype=str)

        # Merge su Risorsa
        merged = pd.merge(df_disponibile, df_dimensione, on='Risorsa', how='inner')

        # Pulizia e formato
        merged['Risorsa'] = merged['Risorsa'].astype(str).str.zfill(4).str[:4]
        merged['Disponibile'] = pd.to_datetime(merged['Disponibile'], errors='coerce')
        merged['Dimensione'] = pd.to_numeric(merged['Dimensione'], errors='coerce')

        merged.dropna(subset=['Disponibile', 'Dimensione'], inplace=True)

        merged.sort_values(by=['Disponibile', 'Dimensione', 'Risorsa'], inplace=True)

        risultati = [
            {
                'risorsa': row['Risorsa'],
                'disponibile': row['Disponibile'].strftime('%d/%m/%y'),
                'dimensione': f"{row['Dimensione']:.2f}"
            }
            for _, row in merged.iterrows()
        ]

        return jsonify(risultati)

    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
