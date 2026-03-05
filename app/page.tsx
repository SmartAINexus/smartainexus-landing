'use client'

import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'

const roles = [
  { id: 'manufacturer', label: "I'm a Manufacturer", icon: '🏭', color: '#00f0ff' },
  { id: 'business', label: "I'm a Business Buyer", icon: '💼', color: '#00bfff' },
  { id: 'individual', label: "I'm an Individual Buyer", icon: '🛒', color: '#1e90ff' },
  { id: 'builder', label: "I'm a Builder", icon: '🪖', color: '#4169e1' },
]

export default function Home() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e17] via-[#0f1a3a] to-black flex items-center justify-center relative overflow-hidden">
      {/* Finom háttér animáció */}
      <div className="absolute inset-0 opacity-10 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_50%,#00f0ff_0%,transparent_50%)]" />
      </div>

      <div className="relative z-10 text-center px-4">
        <h1 className="text-6xl md:text-8xl font-bold text-[#00f0ff] mb-6 tracking-wider animate-pulse">
          SMARTAI NEXUS
        </h1>
        <p className="text-2xl md:text-4xl text-gray-300 mb-16">
          Global Intelligence Platform
        </p>
        <p className="text-xl md:text-2xl text-gray-400 mb-12">
          Find. Build. Buy. Instantly.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
          {roles.map((role) => (
            <motion.div
              key={role.id}
              className="relative p-8 rounded-3xl backdrop-blur-xl border border-[#00f0ff]/30 cursor-pointer overflow-hidden group bg-black/30"
              onClick={() => router.push(`/${role.id}`)}
              initial={{ scale: 1, opacity: 0.9 }}
              whileHover={{
                scale: 1.15,
                opacity: 1,
                boxShadow: `0 0 40px 15px ${role.color}40`,
                transition: { type: 'spring', stiffness: 300, damping: 15 }
              }}
              whileTap={{ scale: 0.98 }}
              transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            >
              {/* Glow hoverkor */}
              <div className="absolute inset-0 bg-gradient-to-br from-transparent via-transparent to-[#00f0ff]/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

              <div className="text-7xl mb-6">{role.icon}</div>
              <h3 className="text-2xl font-semibold text-[#00f0ff]">{role.label}</h3>
            </motion.div>
          ))}
        </div>

        <p className="mt-20 text-xl text-gray-500">
          Launching Soon – Stay Tuned
        </p>
      </div>
    </div>
  )
}
