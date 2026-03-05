"use client";

import { motion } from 'framer-motion';

const roles = [
  { title: "I'm a Manufacturer", icon: '🏭', desc: "Gyártóként használd az AI-t a termelés forradalmasítására." },
  { title: "I'm a Business Buyer", icon: '💼', desc: "Üzleti vevőként találj megbízható partnereket és exkluzív ajánlatokat." },
  { title: "I'm an Individual Buyer", icon: '🛒', desc: "Magánvevőként vásárolj okosan, személyre szabott lehetőségekkel." },
  { title: "I'm a Builder", icon: '🪖', desc: "Építs, tesztelj és alkoss AI segítségével – próbáld ki ingyen!" },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white relative overflow-hidden">
      {/* Finom háttér animáció / particle effekt */}
      <div className="absolute inset-0 opacity-20 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_10%_20%,#00f0ff_0%,transparent_50%)] animate-pulse-slow" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_90%_80%,#ff00aa_0%,transparent_50%)] animate-pulse-slow-delay" />
      </div>

      <div className="relative z-10 container mx-auto px-6 py-24 flex flex-col items-center justify-center min-h-screen">
        {/* Nagy cím */}
        <motion.h1
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.2, ease: "easeOut" }}
          className="text-6xl md:text-9xl font-extrabold mb-6 tracking-[0.2em] bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-500 bg-clip-text text-transparent animate-glow"
        >
          SMARTAI NEXUS
        </motion.h1>

        {/* Alcím */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
          className="text-2xl md:text-4xl text-center mb-8 text-gray-300 max-w-4xl"
        >
          Global Intelligence Platform
        </motion.p>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 1 }}
          className="text-xl md:text-2xl text-center mb-16 text-cyan-300"
        >
          Find. Build. Buy. Instantly.
        </motion.p>

        {/* 4 lebegő kártya */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 w-full max-w-7xl">
          {roles.map((role, index) => (
            <motion.div
              key={role.title}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 + 1, duration: 0.8, ease: "easeOut" }}
              className="group relative bg-black/40 backdrop-blur-2xl border border-cyan-500/20 rounded-3xl p-8 hover:border-cyan-400/60 hover:scale-[1.08] transition-all duration-500 cursor-default shadow-2xl shadow-cyan-900/30"
            >
              {/* Glow és hover effekt */}
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700 rounded-3xl" />

              <div className="text-8xl mb-6 text-center group-hover:scale-110 transition-transform duration-500">
                {role.icon}
              </div>

              <h3 className="text-3xl font-bold text-center mb-4 text-cyan-200 group-hover:text-cyan-100">
                {role.title}
              </h3>

              <p className="text-gray-300 text-center text-lg">
                {role.desc}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Teaser alul */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2, duration: 1 }}
          className="mt-20 text-2xl text-cyan-400 text-center tracking-wide"
        >
          Launching Soon – Stay Tuned
        </motion.p>
      </div>
    </div>
  );
}
