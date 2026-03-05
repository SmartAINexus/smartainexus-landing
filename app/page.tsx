// app/page.tsx
export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white relative overflow-hidden flex flex-col items-center justify-center">
      {/* Háttérkép – most ez a fő vizuális elem */}
      <div
        className="absolute inset-0 bg-cover bg-center opacity-50" // opacity 50% – állítsd 40-60% között tesztelve
        style={{ backgroundImage: "url('/hero-ui.jpg')" }} // pontosan a fájlneved, public gyökerében
      />

      {/* Sötét overlay a jobb olvashatóságért – opcionális, finomhangold */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/70 z-10" />

      {/* Tartalom overlay – középen a cím + szlogen */}
      <div className="relative z-20 text-center px-6 max-w-5xl">
        <h1 className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight text-cyan-400 drop-shadow-2xl">
          SMARTARTAI NEXUS
        </h1>
        <p className="text-2xl md:text-4xl mb-8 font-light opacity-90">
          Global Intelligence Platform
        </p>
        <p className="text-xl md:text-2xl mb-16 opacity-80">
          Find. Build. Buy. Instantly.
        </p>
      </div>

      {/* Interaktív kártyák – pozicionáld őket a background képen látható helyekre */}
      <div className="relative z-30 grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-12 w-full max-w-6xl px-8 mt-[-10%] md:mt-[-5%]">
        {/* Manufacturer kártya – igazítsd a background pozícióhoz */}
        <a
          href="/manufacturer" // később igazi oldal/link
          className="group bg-transparent border border-cyan-500/40 rounded-2xl p-6 md:p-10 flex flex-col items-center justify-center transition-all duration-400 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-600/60 hover:border-cyan-400 hover:bg-black/30 cursor-pointer backdrop-blur-sm"
        >
          <div className="text-6xl md:text-8xl mb-4 transition-transform duration-300 group-hover:rotate-6 group-hover:scale-125">
            🏭
          </div>
          <span className="text-base md:text-xl font-semibold text-cyan-300 group-hover:text-cyan-100">
            Manufacturer
          </span>
        </a>

        {/* Business Buyer */}
        <a
          href="/business-buyer"
          className="group bg-transparent border border-cyan-500/40 rounded-2xl p-6 md:p-10 flex flex-col items-center justify-center transition-all duration-400 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-600/60 hover:border-cyan-400 hover:bg-black/30 cursor-pointer backdrop-blur-sm"
        >
          <div className="text-6xl md:text-8xl mb-4 transition-transform duration-300 group-hover:rotate-6 group-hover:scale-125">
            💼
          </div>
          <span className="text-base md:text-xl font-semibold text-cyan-300 group-hover:text-cyan-100">
            Business Buyer
          </span>
        </a>

        {/* Individual Buyer */}
        <a
          href="/individual-buyer"
          className="group bg-transparent border border-cyan-500/40 rounded-2xl p-6 md:p-10 flex flex-col items-center justify-center transition-all duration-400 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-600/60 hover:border-cyan-400 hover:bg-black/30 cursor-pointer backdrop-blur-sm"
        >
          <div className="text-6xl md:text-8xl mb-4 transition-transform duration-300 group-hover:rotate-6 group-hover:scale-125">
            🛒
          </div>
          <span className="text-base md:text-xl font-semibold text-cyan-300 group-hover:text-cyan-100">
            Individual Buyer
          </span>
        </a>

        {/* Builder */}
        <a
          href="/builder"
          className="group bg-transparent border border-cyan-500/40 rounded-2xl p-6 md:p-10 flex flex-col items-center justify-center transition-all duration-400 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-600/60 hover:border-cyan-400 hover:bg-black/30 cursor-pointer backdrop-blur-sm"
        >
          <div className="text-6xl md:text-8xl mb-4 transition-transform duration-300 group-hover:rotate-6 group-hover:scale-125">
            ⛑️
          </div>
          <span className="text-base md:text-xl font-semibold text-cyan-300 group-hover:text-cyan-100">
            Builder
          </span>
        </a>
      </div>

      {/* Alul a Launching Soon */}
      <div className="relative z-20 mt-auto pb-12 text-center text-lg opacity-70">
        Launching Soon – Stay Tuned
      </div>
    </main>
  );
}
