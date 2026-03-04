export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center relative overflow-hidden">
      {/* Háttérkép + overlay a jobb olvashatóságért */}
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-40" // opacity 30-50% ajánlott, hogy ne legyen túl erős
        style={{ backgroundImage: "url('/hero-bg.jpg')" }} // ide tedd a fájlnevet
      />
      {/* Opcionális gradient overlay extra sötétítéshez */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/70" />

      <div className="relative z-10 text-center px-4 max-w-4xl">
        <h1 className="text-5xl md:text-7xl font-bold mb-4 tracking-tight text-cyan-400">
          SMARTARTAI NEXUS
        </h1>
        <p className="text-2xl md:text-4xl mb-8">
          Global Intelligence Platform
        </p>
        <p className="text-xl md:text-2xl mb-12 opacity-90">
          Find. Build. Buy. Instantly.
        </p>

        {/* Gombok gridben vagy flexben – tedd responszívvá */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-5xl mx-auto">
          {/* Manufacturer gomb */}
          <button className="bg-gray-900/80 border border-cyan-500/30 hover:border-cyan-400 hover:bg-cyan-900/30 transition p-8 rounded-xl flex flex-col items-center">
            <div className="text-5xl mb-4">🏭</div> {/* vagy SVG ikon */}
            <span className="text-lg font-semibold">I'm a Manufacturer</span>
          </button>

          {/* Hasonlóan a többi: Business Buyer, Individual Buyer, Builder */}
          {/* ... másold be a többi gombot */}
        </div>

        <p className="mt-16 text-lg opacity-70">
          Launching Soon – Stay Tuned
        </p>
      </div>
    </main>
  );
}
