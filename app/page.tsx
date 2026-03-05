// app/page.tsx
import Link from 'next/link'; // ha navigáció kell

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center relative overflow-hidden">
      {/* Háttérkép – cseréld a tiedre vagy az egyik keresettre */}
      <div
        className="absolute inset-0 bg-cover bg-center opacity-30" // 30% opacity, hogy ne nyomja el a szöveget
        style={{ backgroundImage: "url('/images/hero-bg.png.jpg')" }} // ide a fájlneved
      />
      {/* Extra sötét overlay a jobb olvashatóságért */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-black/80" />

      <div className="relative z-10 text-center px-6 max-w-5xl">
        <h1 className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight text-cyan-400 drop-shadow-lg">
          SMARTARTAI NEXUS
        </h1>
        <p className="text-2xl md:text-4xl mb-8 font-light">
          Global Intelligence Platform
        </p>
        <p className="text-xl md:text-2xl mb-16 opacity-90">
          Find. Build. Buy. Instantly.
        </p>

        {/* Kattintható kártya/gombok gridben – hover: scale + glow + shadow */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-10">
          {/* Manufacturer */}
          <Link
            href="/manufacturer" // később cseréld igazi útvonalra, most placeholder
            className="group bg-gray-900/60 border border-cyan-500/30 rounded-2xl p-8 flex flex-col items-center justify-center transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50 hover:border-cyan-400/70 hover:bg-gray-800/70 cursor-pointer"
          >
            <div className="text-6xl mb-4 transition-transform duration-300 group-hover:rotate-6">🏭</div>
            <span className="text-lg md:text-xl font-semibold text-cyan-300 group-hover:text-cyan-200">
              I'm a Manufacturer
            </span>
          </Link>

          {/* Business Buyer */}
          <Link
            href="/business-buyer"
            className="group bg-gray-900/60 border border-cyan-500/30 rounded-2xl p-8 flex flex-col items-center justify-center transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50 hover:border-cyan-400/70 hover:bg-gray-800/70 cursor-pointer"
          >
            <div className="text-6xl mb-4 transition-transform duration-300 group-hover:rotate-6">💼</div>
            <span className="text-lg md:text-xl font-semibold text-cyan-300 group-hover:text-cyan-200">
              I'm a Business Buyer
            </span>
          </Link>

          {/* Individual Buyer */}
          <Link
            href="/individual-buyer"
            className="group bg-gray-900/60 border border-cyan-500/30 rounded-2xl p-8 flex flex-col items-center justify-center transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50 hover:border-cyan-400/70 hover:bg-gray-800/70 cursor-pointer"
          >
            <div className="text-6xl mb-4 transition-transform duration-300 group-hover:rotate-6">🛒</div>
            <span className="text-lg md:text-xl font-semibold text-cyan-300 group-hover:text-cyan-200">
              I'm an Individual Buyer
            </span>
          </Link>

          {/* Builder */}
          <Link
            href="/builder"
            className="group bg-gray-900/60 border border-cyan-500/30 rounded-2xl p-8 flex flex-col items-center justify-center transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50 hover:border-cyan-400/70 hover:bg-gray-800/70 cursor-pointer"
          >
            <div className="text-6xl mb-4 transition-transform duration-300 group-hover:rotate-6">⛑️</div>
            <span className="text-lg md:text-xl font-semibold text-cyan-300 group-hover:text-cyan-200">
              I'm a Builder
            </span>
          </Link>
        </div>

        <p className="mt-20 text-lg opacity-70">
          Launching Soon – Stay Tuned
        </p>
      </div>
    </main>
  );
}
