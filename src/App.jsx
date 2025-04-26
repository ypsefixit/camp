import React, { useState, useEffect } from 'react';
import * as XLSX from 'xlsx';
import toast, { Toaster } from 'react-hot-toast';
import { parse, format } from 'date-fns';

function App() {
  const [dimensioni, setDimensioni] = useState([]);
  const [disponibilita, setDisponibilita] = useState([]);
  const [dataFiltro, setDataFiltro] = useState(new Date().toISOString().split('T')[0]);
  const [dimensioneFiltro, setDimensioneFiltro] = useState("5");
  const [risultati, setRisultati] = useState([]);
  const [ricercaEffettuata, setRicercaEffettuata] = useState(false);

  useEffect(() => {
    fetch('/dimensione.xlsx')
      .then(res => res.arrayBuffer())
      .then(data => {
        const workbook = XLSX.read(data);
        const sheet = workbook.Sheets[workbook.SheetNames[0]];
        const json = XLSX.utils.sheet_to_json(sheet);
        setDimensioni(json);
      });
  }, []);

  const handleUploadDimensioni = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      const data = new Uint8Array(evt.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      const sheet = workbook.Sheets[workbook.SheetNames[0]];
      const json = XLSX.utils.sheet_to_json(sheet);
      setDimensioni(json);
      setRicercaEffettuata(false);
      toast.success("✅ Dimensioni aggiornate");
    };
    reader.readAsArrayBuffer(file);
  };

  const handleUploadDisponibilita = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      const data = new Uint8Array(evt.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      const sheet = workbook.Sheets[workbook.SheetNames[0]];
      const json = XLSX.utils.sheet_to_json(sheet);
      setDisponibilita(json);
      setRicercaEffettuata(false);
      toast.success("✅ Disponibilità caricata");
    };
    reader.readAsArrayBuffer(file);
  };

  const handleSearch = () => {
    const mappaDisponibilita = Object.fromEntries(
      disponibilita.map(row => [row.risorsa, row.disponibile])
    );

    const risultatiFiltrati = dimensioni
      .map(row => {
        const dataDisponibile = mappaDisponibilita[row.risorsa];
        const dataDisponibileParsed = dataDisponibile
          ? parse(dataDisponibile, 'dd/MM/yy', new Date())
          : null;

        return {
          ...row,
          disponibile: dataDisponibileParsed
            ? format(dataDisponibileParsed, 'dd/MM/yy')
            : null,
          dataDisponibileParsed
        };
      })
      .filter(row =>
        parseFloat(row.dimensione) >= parseFloat(dimensioneFiltro) &&
        row.dataDisponibileParsed &&
        row.dataDisponibileParsed >= new Date(dataFiltro)
      )
      .sort((a, b) => {
        return (
          a.dataDisponibileParsed - b.dataDisponibileParsed ||
          a.dimensione - b.dimensione ||
          a.risorsa.localeCompare(b.risorsa)
        );
      });

    setRisultati(risultatiFiltrati);
    setRicercaEffettuata(true);
  };

  return (
    <div className="p-4 max-w-md mx-auto space-y-4">
      <Toaster />
      <img src="/logo.jpeg" alt="Logo" className="w-32 mx-auto" />
      <h1 className="text-center text-2xl font-bold">CAMPEGGIO SANTA MARGHERITA</h1>

      <div className="space-y-2 border-t pt-4">
        <input
          type="date"
          value={dataFiltro}
          onChange={e => setDataFiltro(e.target.value)}
          className="w-full p-2 border rounded"
        />
        <select
          value={dimensioneFiltro}
          onChange={e => setDimensioneFiltro(e.target.value)}
          className="w-full p-2 border rounded"
        >
          {[...Array(9)].map((_, i) => {
            const val = (5 + i * 0.5).toFixed(1);
            return <option key={val} value={val}>{val}</option>;
          })}
        </select>
        <button
          onClick={handleSearch}
          className="w-full p-2 bg-blue-600 text-white rounded"
        >
          Cerca
        </button>
      </div>

      <div className="space-y-2">
        {risultati.length > 0 ? (
          <table className="w-full text-sm border mt-4">
            <thead>
              <tr className="bg-gray-100">
                <th className="border px-2 py-1">Risorsa</th>
                <th className="border px-2 py-1">Dimensione</th>
                <th className="border px-2 py-1">Disponibile</th>
              </tr>
            </thead>
            <tbody>
              {risultati.map((row, i) => (
                <tr key={i}>
                  <td className="border px-2 py-1">{row.risorsa}</td>
                  <td className="border px-2 py-1">{row.dimensione}</td>
                  <td className="border px-2 py-1">{row.disponibile}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          ricercaEffettuata && (
            <div className="text-center text-sm text-gray-500 mt-4">
              Nessuna risorsa trovata con i criteri selezionati.
            </div>
          )
        )}
      </div>

      <div className="space-y-2 border-t pt-4">
        <label className="block text-sm">📤 Carica nuovo <strong>Disponibilità Risorse</strong></label>
        <input type="file" accept=".xlsx" onChange={handleUploadDisponibilita} />

        <label className="block text-sm mt-4">📤 Carica nuovo <strong>Dimensioni Risorse</strong></label>
        <input type="file" accept=".xlsx" onChange={handleUploadDimensioni} />
      </div>
    </div>
  );
}

export default App;