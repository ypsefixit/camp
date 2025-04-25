from flask import Flask, request, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Funzione per caricare il file dimensione
def load_dimensione():
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'dimensione.xlsx')
    if os.path.exists(path):
        try:
            return pd.read_excel(path)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_disponibile', methods=['POST'])
def upload_disponibile():
    file = request.files.get('file')
    if file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'disponibile.xlsx')
        file.save(path)
        return jsonify({'success': True, 'message': 'File disponibile caricato con successo'})
    return jsonify({'success': False, 'message': 'Errore nel caricamento'})

@app.route('/upload_dimensione', methods=['POST'])
def upload_dimensione():
    file = request.files.get('file')
    if file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'dimensione.xlsx')
        file.save(path)
        return jsonify({'success': True, 'message': 'File dimensione aggiornato con successo'})
    return jsonify({'success': False, 'message': 'Nessun file caricato'})

@app.route('/cerca', methods=['POST'])
def cerca():
    try:
        disponibile = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], 'disponibile.xlsx'))
        dimensione_df = load_dimensione()
        if dimensione_df.empty:
            return jsonify([])
        merged = disponibile.merge(dimensione_df, on='risorsa', how='left')
        merged = merged.sort_values(by=['disponibile', 'dimensione', 'risorsa'])
        results = merged.to_dict(orient='records')
        return jsonify(results)
    except Exception as e:
        print("Errore:", e)
        return jsonify([])
