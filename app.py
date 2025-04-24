
import pandas as pd
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

merged_data = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_disponibile', methods=['POST'])
def upload_disponibile():
    global merged_data
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.lower()
    df['disponibile'] = pd.to_datetime(df['disponibile'], dayfirst=True)
    if merged_data.empty:
        merged_data = df
    else:
        merged_data = pd.merge(merged_data, df, on='risorsa')
    return 'File caricato con successo'

@app.route('/upload_dimensione', methods=['POST'])
def upload_dimensione():
    global merged_data
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.lower()
    df['dimensione'] = df['dimensione'].astype(str).str.replace(',', '.').astype(float)
    if merged_data.empty:
        merged_data = df
    else:
        merged_data = pd.merge(merged_data, df, on='risorsa')
    return 'File caricato con successo'

@app.route('/search', methods=['POST'])
def search():
    global merged_data
    data_filter = request.form.get('data')
    dimensione_filter = request.form.get('dimensione')

    print(f"Numero totale righe in merged_data: {len(merged_data)}")
    results = merged_data.copy()

    if data_filter:
        try:
            data_dt = pd.to_datetime(data_filter, dayfirst=True)
            print(f"Filtro per data: {data_dt.strftime('%d/%m/%y')}")
            results = results[results['disponibile'] >= data_dt]
        except Exception as e:
            print(f"Errore nel parsing della data: {e}")

    if dimensione_filter:
        try:
            dim = float(dimensione_filter.replace(',', '.'))
            print(f"Filtro per dimensione >= {dim}")
            results = results[results['dimensione'] >= dim]
        except Exception as e:
            print(f"Errore nella conversione della dimensione: {e}")

    results = results.sort_values(by=['risorsa', 'disponibile', 'dimensione'], ascending=[True, True, True])
    print(f"Numero risultati dopo filtri: {len(results)}")
    return results.to_json(orient='records')
