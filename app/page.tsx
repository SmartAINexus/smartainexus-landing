// app/page.tsx – teljes fájl, másold be és mentsd

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white flex flex-col items-center justify-center">
      <h1 className="text-7xl md:text-9xl font-extrabold mb-8 bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
        SMARTARTAI NEXUS
      </h1>
      <p className="text-3xl md:text-5xl mb-16 text-center text-gray-300 max-w-4xl">
        Global Intelligence Platform — Find. Build. Buy. Instantly.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 w-full max-w-7xl px-6">
        {[
          { title: "I'm a Manufacturer", desc: "Gyártóként csatlakozz..." },
          { title: "I'm a Business Buyer", desc: "Üzleti vevőként találj..." },
          { title: "I'm an Individual Buyer", desc: "Magánvevőként vásárolj..." },
          { title: "I'm a Builder", desc: "Építs és tesztelj..." },
        ].map((item) => (
          <div
            key={item.title}
            className="group relative bg-gray-900/50 backdrop-blur-xl border border-cyan-500/30 rounded-2xl p-8 hover:border-cyan-400 hover:scale-105 transition-all duration-500 cursor-pointer shadow-2xl"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl" />
            <h3 className="text-3xl font-bold text-center mb-4 text-cyan-300 group-hover:text-cyan-100">
              {item.title}
            </h3>
            <p className="text-gray-400 text-center">
              {item.desc}
            </p>
          </div>
        ))}
      </div>

      <p className="mt-20 text-2xl text-gray-400">
        Launching Soon – Stay Tuned
      </p>
    </div>
  )
}
