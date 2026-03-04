'use client';

import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';

const roles = [
  { id: 'manufacturer', label: "I'm a Manufacturer", icon: '🏭' },
  { id: 'business', label: "I'm a Business Buyer", icon: '💼' },
  { id: 'individual', label: "I'm an Individual Buyer", icon: '🛒' },
  { id: 'builder', label: "I'm a Builder", icon: '🪖' },
];

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e17] via-[#0f1a3a] to-black flex items-center justify-center overflow-hidden px-4">
      {/* Háttér finom animáció */}
      <div className="absolute inset-0 opacity-10 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_50%,#00f0ff_0%,transparent_50%)] animate-pulse-slow" />
      </div>

      <div className="relative z-10 text-center">
        <h1 className="text-6xl md:text-8xl font-bold text-[#00f0ff] tracking-wider mb-6 animate-glow">
          SMARTAI NEXUS
        </h1>
        <p className="text-2xl md:text-4xl text-gray-300 mb-12">
          Global Intelligence Platform
        </p>
        <p className="text-xl md:text-2xl text-gray-400 mb-16">
          Find. Build. Buy. Instantly.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8 max-w-6xl mx-auto">
          {roles.map((role) => (
            <motion.div
              key={role.id}
              className="bg-black/40 border border-[#00f0ff]/30 p-8 md:p-10 rounded-3xl cursor-pointer backdrop-blur-xl hover:border-[#00f0ff] group"
              onClick={() => router.push(`/${role.id}`)}
              initial={{ scale: 1, opacity: 0.9 }}
              whileHover={{
                scale: 1.12,
                boxShadow: '0 0 40px 15px rgba(0, 240, 255, 0.4)',
                transition: { type: 'spring', stiffness: 300, damping: 15 }
              }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="text-7xl md:text-8xl mb-6 transition-transform group-hover:scale-110">
                {role.icon}
              </div>
              <h3 className="text-xl md:text-2xl font-semibold text-white">
                {role.label}
              </h3>
            </motion.div>
          ))}
        </div>

        <p className="mt-16 text-lg md:text-xl text-gray-500">
          Launching Soon – Stay Tuned
        </p>
      </div>
    </div>
  );
}
