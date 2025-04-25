# Campeggio Santa Margherita

Webapp responsive per la gestione di risorse con caricamento e filtro da file Excel.

## 🚀 Funzionalità
- Caricamento iniziale automatico del file `dimensione.xlsx`
- Form per caricare nuovi file Excel (dimensioni e disponibilità)
- Filtro per data e dimensione minima
- Visualizzazione risultati ordinati
- Mobile responsive
- Deployabile facilmente su Render.com

## 📦 Requisiti
- Node.js >= 16
- npm

## ▶️ Avvio in locale
```bash
npm install
npm run dev
```

## 🚀 Deploy su Render.com
1. Carica questo progetto su GitHub
2. Su [Render](https://render.com), crea un nuovo servizio **Static Site**
3. Imposta:
   - Build command: `npm run build`
   - Publish directory: `dist`
4. Fai deploy!

## 📁 File Excel
- `dimensione.xlsx` va inserito in `public/` (sarà caricato all'avvio)
- I file caricati tramite form aggiorneranno i dati temporaneamente (solo frontend)

Enjoy!
