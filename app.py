
from flask import Flask, request, render_template, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__, static_folder='static')

df_disponibile = pd.DataFrame()
df_dimensione = pd.DataFrame()
merged_data = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_disponibile', methods=['POST'])
def upload_disponibile():
    global df_disponibile, merged_data
    try:
        file = request.files['file']
        df = pd.read_excel(file)
        df['risorsa'] = df['risorsa'].astype(str).str.strip().str.upper()
        df['disponibile'] = pd.to_datetime(df['disponibile'], dayfirst=True, errors='coerce')
        df_disponibile = df

        merged = pd.merge(df_dimensione, df_disponibile, on='risorsa', how='left')
        merged['disponibile'] = merged['disponibile'].fillna(pd.to_datetime(datetime.now().strftime("%d/%m/%y"), dayfirst=True))
        merged_data[:] = merged

        return 'File "disponibile" caricato con successo.'

@app.route('/upload_dimensione', methods=['POST'])
def upload_dimensione():
    global df_dimensione, merged_data

    file = request.files['file']
    df = pd.read_excel(file)
    df['risorsa'] = df['risorsa'].astype(str).str.strip().str.upper()
    df['dimensione'] = df['dimensione'].astype(str).str.replace(',', '.').astype(float)
    df_dimensione = df

    merged = pd.merge(df_dimensione, df_disponibile, on='risorsa', how='left')
    merged['disponibile'] = merged['disponibile'].fillna(pd.to_datetime(datetime.now().strftime("%d/%m/%y"), dayfirst=True))
    merged_data[:] = merged

    return 'File "disponibile" caricato con successo.'

@app.route('/search', methods=['GET'])
def search():
    global merged_data

    data = request.args.get('data')
    dimensione = request.args.get('dimensione')

    results = merged_data.copy()


    if data:
        try:
            data_dt = datetime.strptime(data, "%d/%m/%y")
            results = results[results['disponibile'] >= data_dt]
        except:
            return jsonify([])
    
    
    if dimensione:
        try:
            dim = float(dimensione.replace(',', '.'))
            results = results[results['dimensione'] == dim]
        except:
            return jsonify([])

    return results.to_json(orient='records')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
