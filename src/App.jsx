import React, { useState, useEffect } from 'react';
import * as XLSX from 'xlsx';
import toast, { Toaster } from 'react-hot-toast';

function App() {
  const [dimensioni, setDimensioni] = useState([]);

const parseDate = (str) => {
    const [day, month, year] = str.split('/');
    return new Date(`20${year}`, month - 1, day);
  };
  const [disponibilita, setDisponibilita] = useState([]);
  const [dataFiltro, setDataFiltro] = useState(new Date().toISOString().split('T')[0]);
  const [dimensioneFiltro, setDimensioneFiltro] = useState("5");
  const [risultati, setRisultati] = useState([]);

const formatToday = () => {
  const today = new Date();
  const day = String(today.getDate()).padStart(2, '0');
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const year = String(today.getFullYear()).slice(-2);
  return `${day}/${month}/${year}`;
};

const parseDDMMYY = str => {
  const [day, month, year] = str.split('/');
  const fullYear = parseInt(year.length === 2 ? '20' + year : year, 10);
  return new Date(fullYear, parseInt(month) - 1, parseInt(day));
};

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
      toast.success("✅ Disponibilità caricata");
    };
    reader.readAsArrayBuffer(file);
  };

  const handleSearch = () => {
    const mappaDisponibilita = Object.fromEntries(disponibilita.map(row => [row.risorsa, row.disponibile]));
    const risultatiFiltrati = dimensioni
      .map(row => ({
        ...row,
        disponibile: mappaDisponibilita[row.risorsa]
      }))
      .filter(row =>
        parseFloat(row.dimensione) >= parseFloat(dimensioneFiltro) &&
        row.disponibile &&
        parseDDMMYY(row.disponibile) >= new Date(dataFiltro)
      )
      .sort((a, b) => {
        const da = parseDDMMYY(a.disponibile);
        const db = parseDDMMYY(b.disponibile);
        return da - db || a.dimensione - b.dimensione || a.risorsa.localeCompare(b.risorsa);
      });

    setRisultati(risultatiFiltrati);
  };

  return (
    <div className="p-4 max-w-md mx-auto space-y-4">
      <Toaster />
      <img src="/logo.jpeg" alt="Logo" className="w-32 mx-auto" />
      <h1 className="text-center text-2xl font-bold">CAMPEGGIO SANTA MARGHERITA</h1>

      <div className="space-y-2 border-t pt-4">
        <label className="block font-semibold">DISPONIBILE FINO AL:</label>
<input type="date" value={dataFiltro} onChange={e => setDataFiltro(e.target.value)} className="w-full p-2 border rounded" />
        <label className="block font-semibold mt-2">LUNGHEZZA IN METRI</label>
<select value={dimensioneFiltro} onChange={e => setDimensioneFiltro(e.target.value)} className="w-full p-2 border rounded">
          {[...Array(9)].map((_, i) => {
            const val = (5 + i * 0.5).toFixed(1);
            return <option key={val} value={val}>{val}</option>;
          })}
        </select>
        <button onClick={handleSearch} className="w-full p-2 bg-blue-600 text-white rounded">Cerca</button>
      </div>

<div className="space-y-4 border-t pt-4 mt-4">
  <div>
    <label className="block font-semibold mb-1">Carica file DISPONIBILITÀ (risorsa + disponibile):</label>
    <input type="file" accept=".xlsx, .xls" onChange={handleFileUpload} className="border p-2 w-full" />
  </div>
  <div>
    <label className="block font-semibold mb-1">Carica file COMPLETO (risorsa + dimensione + disponibile):</label>
    <input type="file" accept=".xlsx, .xls" onChange={handleFullReplace} className="border p-2 w-full" />
  </div>
</div>


      <div className="space-y-2">
        {risultati.length > 0 && (
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
