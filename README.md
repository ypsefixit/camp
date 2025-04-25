# Campeggio Santa Margherita - WebApp

Questa applicazione consente di caricare file Excel, aggiornare dati e cercare disponibilità all'interno del sistema campeggio.

## 📁 Struttura del Progetto

```
campeggio/
├── app.py               # Backend Flask
├── index.html           # Interfaccia web
├── requirements.txt     # Dipendenze Python
├── render.yaml          # Configurazione deploy Render
└── uploads/             # Cartella per file Excel caricati
```

## 🚀 Come Avviare in Locale

1. Clona il repository:
   ```bash
   git clone https://github.com/tuo-utente/campeggio.git
   cd campeggio
   ```

2. Crea un ambiente virtuale (opzionale ma consigliato):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts\activate
   ```

3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

4. Avvia il server:
   ```bash
   python app.py
   ```

5. Apri il browser su `http://localhost:5000`

## 🌐 Deploy su Render

1. Carica i file su un repository GitHub.
2. Vai su [https://render.com](https://render.com) > New Web Service.
3. Collega il repo e conferma la configurazione.
4. Render userà automaticamente `render.yaml`.

## 📂 Upload Files

- `disponibile.xlsx`: file caricato tramite form per la disponibilità.
- `dimensione.xlsx`: caricato all’avvio ma aggiornabile da form.

## 📋 Formato Dati

| Campo       | Formato              |
|-------------|----------------------|
| Risorsa     | Testo (4 lettere)    |
| Disponibile | Data (gg/mm/aa)      |
| Dimensione  | Numero (2 decimali)  |

---

Creato con ❤️ per gestire al meglio le disponibilità del campeggio.