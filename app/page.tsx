'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

const roles = [
  { id: 'manufacturer', label: "I'm a Manufacturer", icon: '🏭', color: 'cyan' },
  { id: 'business', label: "I'm a Business Buyer", icon: '💼', color: 'blue' },
  { id: 'individual', label: "I'm an Individual Buyer", icon: '🛒', color: 'yellow' },
  { id: 'builder', label: "I'm a Builder", icon: '🪖', color: 'purple' },
]

export default function Home() {
  const [hovered, setHovered] = useState<string | null>(null)
  const router = useRouter()

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-blue-950 to-black flex items-center justify-center relative overflow-hidden">
      {/* Háttér: ipari szektorok finom animációval */}
      <div className="absolute inset-0 opacity-20 pointer-events-none">
        <motion.div
          className="absolute inset-0 bg-[url('/energy-bg.jpg')] bg-cover"
          animate={{ scale: hovered ? 1.05 : 1 }}
          transition={{ duration: 8, repeat: Infinity, repeatType: 'reverse' }}
        />
        {/* További szektor háttérképek overlay-ként */}
      </div>

      <div className="relative z-10 text-center">
        <h1 className="text-7xl font-bold text-cyan-300 mb-4 tracking-wider">
          INDUSTRO
        </h1>
        <p className="text-3xl text-gray-300 mb-16">Find. Build. Buy. Instantly.</p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-6xl mx-auto">
          {roles.map((role) => (
            <motion.div
              key={role.id}
              className={`relative p-8 rounded-2xl backdrop-blur-xl border border-${role.color}-500/30 cursor-pointer overflow-hidden group`}
              onHoverStart={() => setHovered(role.id)}
              onHoverEnd={() => setHovered(null)}
              onClick={() => router.push(`/${role.id}`)}
              initial={{ scale: 1, opacity: 0.9 }}
              whileHover={{
                scale: 1.15,
                opacity: 1,
                boxShadow: `0 0 40px 10px rgba(0, 255, 255, 0.4)`,
                transition: { type: 'spring', stiffness: 300, damping: 15 }
              }}
              whileTap={{ scale: 0.98 }}
              transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            >
              {/* Glow effekt hoverkor */}
              <div className="absolute inset-0 bg-gradient-to-br from-transparent via-transparent to-cyan-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

              <div className="text-6xl mb-4">{role.icon}</div>
              <h3 className={`text-2xl font-semibold text-${role.color}-300`}>{role.label}</h3>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}
