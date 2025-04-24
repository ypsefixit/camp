from flask import Flask, request, render_template, jsonify
import pandas as pd
from datetime import datetime
app = Flask(__name__, static_folder='static')

try:
    import os
    dimensione_path = os.path.join(os.path.dirname(__file__), 'dimensione.xlsx')
    df = pd.read_excel(dimensione_path)
    df['risorsa'] = df['risorsa'].astype(str).str.strip().str.upper()
    df_dimensione = df
    merged_data = df_dimensione.copy()
    print("✅ Caricamento completato. Righe:", len(merged_data))

    print("✅ File dimensione.xlsx caricato correttamente all'avvio.")
except Exception as e:
    print(f"❌ Errore nel caricamento iniziale di dimensione.xlsx: {e}")
df_disponibile = pd.DataFrame()
df_dimensione = pd.DataFrame()
merged_data = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_disponibile', methods=['POST'])
def upload_disponibile():
    file = request.files['file']
    if not file:
        return jsonify({'success': False, 'message': '❌ Nessun file selezionato.'}), 400
    try:
        df = pd.read_excel(file)
        df['risorsa'] = df['risorsa'].astype(str).str.strip().str.upper()
        df['disponibile'] = pd.to_datetime(df['disponibile'], dayfirst=True, errors='coerce')
        df_disponibile = df
        merged = pd.merge(df_dimensione, df_disponibile, on='risorsa', how='left')
        merged['disponibile'] = merged['disponibile'].fillna(pd.to_datetime(datetime.now().strftime('%d/%m/%y'), dayfirst=True))
        merged_data = merged
        return 'File "disponibile" caricato con successo.'
    except Exception as e:
        print(f'Errore: {e}')
        return 'Errore durante il caricamento del file disponibile.'

@app.route('/upload_dimensione', methods=['POST'])
def upload_dimensione():
    file = request.files['file']
    if not file:
        return jsonify({'success': False, 'message': '❌ Nessun file selezionato.'}), 400
    try:
        df = pd.read_excel(file)
        df['risorsa'] = df['risorsa'].astype(str).str.strip().str.upper()
        df['dimensione'] = df['dimensione'].astype(str).str.replace(',', '.').astype(float)
        df_dimensione = df
        merged = pd.merge(df_dimensione, df_disponibile, on='risorsa', how='left')
        merged['disponibile'] = merged['disponibile'].fillna(pd.to_datetime(datetime.now().strftime('%d/%m/%y'), dayfirst=True))
        merged_data = merged
        return 'File "dimensione" caricato con successo.'
    except Exception as e:
        print(f'Errore: {e}')
        return 'Errore durante il caricamento del file dimensione.'

@app.route('/search', methods=['POST'])
def search():
    global merged_data
    date = request.form.get('date')
    dimensione = request.form.get('dimensione')
    try:
        filtered = merged_data.copy()
        if date:
            filtered = filtered[filtered['Data'] == date]
        if dimensione:
            filtered = filtered[filtered['Dimensione'] == float(dimensione)]
        filtered = filtered.sort_values(by='Dimensione', ascending=True)
        data = filtered.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500