# Campeggio Santa Margherita

Web app per la gestione della disponibilità risorse. Carica due file `.xlsx`, uno per la disponibilità e uno per le dimensioni.

## Funzionalità

- Caricamento file "disponibile.xlsx"
- Aggiornamento file "dimensione.xlsx"
- Ricerca e visualizzazione risultati

## Deploy su Render

1. Carica il progetto su GitHub.
2. Connetti il repo su [render.com](https://render.com).
3. Imposta i comandi nel `render.yaml`.
4. Premi "Clear cache and deploy" in caso di problemi.

## Requisiti

- Flask
- Pandas
- Gunicorn
- OpenPyXL
