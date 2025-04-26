# Campeggio Santa Margherita

Questa è una web app React per la gestione della disponibilità delle risorse.

## 🧩 Funzionalità principali
- Ricerca per data e lunghezza in metri
- Caricamento file `disponibilità.xlsx`
- Aggiornamento completo tramite file `risorse.xlsx`
- Risultati ordinati per disponibilità, dimensione e nome

## 🚀 Deploy su Render (Static Site)

1. **Installazione locale:**
   ```bash
   npm install
   ```

2. **Build dell'app:**
   ```bash
   npm run build
   ```

3. **Deploy su Render:**
   - Tipo: **Static Site**
   - Cartella pubblicata: `dist/`
   - Build Command: `npm install && npm run build`
   - No Start Command (statico)

## 🛠️ Configurazione Vite
È incluso `vite.config.js` con `base: './'` per garantire corretto funzionamento delle rotte in ambienti come Render.

---

ℹ️ Assicurati che il file `risorse.xlsx` si trovi in `public/` con tre colonne: `risorsa`, `dimensione`, `disponibile`.