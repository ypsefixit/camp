from flask import Flask, request, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dimensione_df = None

@app.before_first_request
def load_dimensione():
    global dimensione_df
    try:
        dimensione_df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], 'dimensione.xlsx'))
    except Exception:
        dimensione_df = pd.DataFrame()

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
    global dimensione_df
    file = request.files.get('file')
    if file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'dimensione.xlsx')
        file.save(path)
        try:
            dimensione_df = pd.read_excel(path)
            return jsonify({'success': True, 'message': 'File dimensione aggiornato con successo'})
        except Exception:
            return jsonify({'success': False, 'message': 'Errore nella lettura del file dimensione'})
    return jsonify({'success': False, 'message': 'Nessun file caricato'})

@app.route('/cerca', methods=['POST'])
def cerca():
    try:
        disponibile = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], 'disponibile.xlsx'))
        if dimensione_df is None or dimensione_df.empty:
            return jsonify([])
        merged = disponibile.merge(dimensione_df, on='risorsa', how='left')
        merged = merged.sort_values(by=['disponibile', 'dimensione', 'risorsa'])
        results = merged.to_dict(orient='records')
        return jsonify(results)
    except Exception:
        return jsonify([])
