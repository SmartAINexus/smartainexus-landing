"use client";

import { useState } from 'react';

export default function BuilderDemo() {
  const [projectName, setProjectName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleBuild = async () => {
    if (!projectName.trim() || !description.trim()) {
      setError('Add meg a projekt nevét és a leírást!');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Szimulált AI válasz – később igazi API hívás jöhet ide
      await new Promise(resolve => setTimeout(resolve, 2500)); // 2.5 mp "gondolkodás"

      const aiResponse = `
Projekt: ${projectName}

Leírás összefoglaló: ${description}

AI-generált építési vázlat (demo verzió):
- Becsült méret: 450 m² (közepes iroda / lakóépület)
- Anyagok javaslat:
  - Beton alap: 320 m³
  - Acél váz: 18 tonna
  - Üveg homlokzat: 280 m²
  - Napelem integráció: 45 kW teljesítmény (ajánlott)
- Időtartam: 38-52 nap (időjárás függvényében)
- Költségbecslés: 28–42 millió Ft (2026-os árakon, AI-optimalizált)
- Javasolt optimalizálás:
  +22% energiahatékonyság okos rendszerekkel
  -15% költség fenntartható anyagokkal
- Kockázatok: anyaghiány (acél +8% árnövekedés esélye), esős időszak (+7 nap csúszás)

Ez egy ingyenes demo – 1 próbaalkalom regisztráció nélkül. Több építéshez regisztráció szükséges.
      `;

      setResult(aiResponse.trim());
    } catch (err) {
      setError('Hiba történt a generálás során. Próbáld újra!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white flex items-center justify-center p-6">
      <div className="w-full max-w-5xl bg-black/50 backdrop-blur-2xl border border-cyan-500/30 rounded-3xl p-10 md:p-16 shadow-2xl">
        <h1 className="text-5xl md:text-7xl font-extrabold text-center mb-10 bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-500 bg-clip-text text-transparent animate-pulse">
          BUILDER DEMO
        </h1>

        <p className="text-xl md:text-2xl text-center mb-12 text-cyan-300">
          Építs AI segítségével – ingyenes próba 1x!
        </p>

        <div className="space-y-10">
          {/* Projekt név */}
          <div>
            <label className="block text-2xl font-semibold mb-4 text-cyan-200">
              Projekt neve
            </label>
            <input
              type="text"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="Példa: Okos családi ház Budapesten"
              className="w-full p-5 bg-gray-900/70 border border-cyan-500/40 rounded-xl text-white text-xl focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-500/50 transition"
            />
          </div>

          {/* Leírás */}
          <div>
            <label className="block text-2xl font-semibold mb-4 text-cyan-200">
              Rövid leírás / cél
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Írd le, mit szeretnél építeni, hol, milyen méretben, milyen anyagokkal, költségvetéssel stb..."
              rows={7}
              className="w-full p-5 bg-gray-900/70 border border-cyan-500/40 rounded-xl text-white text-xl focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-500/50 transition resize-none"
            />
          </div>

          {/* Gomb */}
          <div className="text-center pt-6">
            <button
              onClick={handleBuild}
              disabled={loading}
              className="px-16 py-7 bg-gradient-to-r from-cyan-600 to-purple-700 hover:from-cyan-500 hover:to-purple-600 text-white text-2xl font-bold rounded-full shadow-2xl transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'AI dolgozik...' : 'ÉPÍTÉS INDÍTÁSA (INGYEN PRÓBA)'}
            </button>
          </div>

          {/* Hiba */}
          {error && (
            <p className="text-red-400 text-center text-xl mt-8">{error}</p>
          )}

          {/* Eredmény */}
          {result && (
            <div className="mt-12 p-10 bg-black/70 border border-cyan-500/40 rounded-2xl">
              <h2 className="text-4xl font-bold text-cyan-300 mb-8 text-center">
                AI-generált építési vázlat
              </h2>
              <pre className="text-gray-200 text-lg whitespace-pre-wrap font-mono leading-relaxed">
                {result}
              </pre>
            </div>
          )}

          {/* Info szöveg alul */}
          <p className="text-center text-xl text-gray-400 mt-16">
            Ez egy ingyenes demo verzió – regisztráció nélkül 1x kipróbálható. Több építéshez később regisztráció szükséges.
          </p>
        </div>
      </div>
    </div>
  );
}
