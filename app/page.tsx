// app/page.tsx
export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-950 via-indigo-950 to-black flex items-center justify-center p-4 md:p-8">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-10 max-w-7xl w-full">
        
        {/* Manufacturer kártya */}
        <a
          href="/manufacturer" // később cseréld igazi útvonalra vagy # -ra ha placeholder
          className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-cyan-900/30 to-blue-900/20 border border-cyan-500/40 backdrop-blur-md transition-all duration-500 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/60 hover:border-cyan-400/70 hover:-translate-y-4 cursor-pointer"
        >
          <div className="p-8 md:p-12 flex flex-col items-center text-center">
            <div className="text-7xl md:text-9xl mb-6 transition-transform duration-500 group-hover:rotate-6 group-hover:scale-125">
              🏭
            </div>
            <h3 className="text-xl md:text-2xl font-bold text-cyan-300 group-hover:text-cyan-100 tracking-wide">
              MANUFACTURER
            </h3>
          </div>
        </a>

        {/* Business Buyer */}
        <a
          href="/business-buyer"
          className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-cyan-900/30 to-blue-900/20 border border-cyan-500/40 backdrop-blur-md transition-all duration-500 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/60 hover:border-cyan-400/70 hover:-translate-y-4 cursor-pointer"
        >
          <div className="p-8 md:p-12 flex flex-col items-center text-center">
            <div className="text-7xl md:text-9xl mb-6 transition-transform duration-500 group-hover:rotate-6 group-hover:scale-125">
              💼
            </div>
            <h3 className="text-xl md:text-2xl font-bold text-cyan-300 group-hover:text-cyan-100 tracking-wide">
              BUSINESS BUYER
            </h3>
          </div>
        </a>

        {/* Individual Buyer */}
        <a
          href="/individual-buyer"
          className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-cyan-900/30 to-blue-900/20 border border-cyan-500/40 backdrop-blur-md transition-all duration-500 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/60 hover:border-cyan-400/70 hover:-translate-y-4 cursor-pointer"
        >
          <div className="p-8 md:p-12 flex flex-col items-center text-center">
            <div className="text-7xl md:text-9xl mb-6 transition-transform duration-500 group-hover:rotate-6 group-hover:scale-125">
              🛒
            </div>
            <h3 className="text-xl md:text-2xl font-bold text-cyan-300 group-hover:text-cyan-100 tracking-wide">
              INDIVIDUAL BUYER
            </h3>
          </div>
        </a>

        {/* Builder */}
        <a
          href="/builder"
          className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-cyan-900/30 to-blue-900/20 border border-cyan-500/40 backdrop-blur-md transition-all duration-500 hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/60 hover:border-cyan-400/70 hover:-translate-y-4 cursor-pointer"
        >
          <div className="p-8 md:p-12 flex flex-col items-center text-center">
            <div className="text-7xl md:text-9xl mb-6 transition-transform duration-500 group-hover:rotate-6 group-hover:scale-125">
              ⛑️
            </div>
            <h3 className="text-xl md:text-2xl font-bold text-cyan-300 group-hover:text-cyan-100 tracking-wide">
              BUILDER
            </h3>
          </div>
        </a>

      </div>
    </main>
  )
}
