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
        merged_data = merged

        return 'File "disponibile" caricato correttamente!'
    except Exception as e:
        return f'Errore: {str(e)}'

@app.route('/upload_dimensione', methods=['POST'])
def upload_dimensione():
    global df_dimensione, merged_data
    try:
        file = request.files['file']
        df = pd.read_excel(file)
        df['risorsa'] = df['risorsa'].astype(str).str.strip().str.upper()
        df_dimensione = df

        merged = pd.merge(df_dimensione, df_disponibile, on='risorsa', how='left')
        merged['disponibile'] = merged['disponibile'].fillna(pd.to_datetime(datetime.now().strftime("%d/%m/%y"), dayfirst=True))
        merged_data = merged

        return 'File "dimensione" caricato correttamente!'
    except Exception as e:
        return f'Errore: {str(e)}'

@app.route('/get_data', methods=['GET'])
def get_data():
    global merged_data
    data_to_return = merged_data.copy()
    data_to_return['disponibile'] = data_to_return['disponibile'].dt.strftime('%d/%m/%Y')
    sorted_data = data_to_return.sort_values(by=['disponibile', 'dimensione', 'risorsa'])
    return jsonify(sorted_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
