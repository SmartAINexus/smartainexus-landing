"use client";

import { useState } from 'react';
import { motion } from 'framer-motion';

export default function BuilderDemo() {
  const [projectName, setProjectName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleBuild = async () => {
    if (!projectName.trim() || !description.trim()) {
      setError('Enter project name and description');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Simulated Grok AI response – replace with real API later
      await new Promise(resolve => setTimeout(resolve, 3200));

      const aiResponse = `
PROJECT: ${projectName}

DESCRIPTION SUMMARY: ${description}

GROK-2100 CONSTRUCTION PROTOCOL (Quantum-AI Optimized):

• Structural Integrity: 99.4% (self-assembling metamaterials + neural lattice reinforcement)
• Core Materials: 580 m³ adaptive nano-concrete, 19.7 tons graphene-titanium hybrid frame
• Energy Matrix: +68% efficiency (zero-point micro-reactors + orbital solar weave)
• Timeline: 21 days (swarm nanobot construction + temporal compression scheduling)
• Total Estimated Cost: $3.94M (AI-negotiated quantum supply chain)
• Enhancement Modules: Holographic adaptive interiors, consciousness-linked control interface
• Risk Assessment: Minimal (quantum entanglement redundancy: 0.3% failure probability)

This is a free prototype build. One trial per session. Register for unlimited protocol access.
      `;

      setResult(aiResponse.trim());
    } catch (err) {
      setError('Protocol initialization failed. Retry.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* 2050-2100 floating holographic particles & geometry */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Lebegő neon részecskék */}
        {Array.from({ length: 20 }).map((_, i) => (
          <motion.div
            key={`particle-${i}`}
            className="absolute w-1.5 h-1.5 bg-cyan-300 rounded-full blur-md"
            initial={{ opacity: 0.1 }}
            animate={{
              x: [Math.random() * 2000 - 1000, Math.random() * 2000 - 1000],
              y: [Math.random() * 2000 - 1000, Math.random() * 2000 - 1000],
              opacity: [0.1, 0.7, 0.1],
              scale: [0.5, 1.8, 0.5],
            }}
            transition={{
              duration: 40 + Math.random() * 60,
              repeat: Infinity,
              ease: "linear",
            }}
          />
        ))}

        {/* Lebegő geometriai formák */}
        {Array.from({ length: 6 }).map((_, i) => (
          <motion.div
            key={`geo-${i}`}
            className="absolute w-32 h-32 border-2 border-purple-500/30 rounded-full blur-xl"
            initial={{ opacity: 0.05, scale: 0.8 }}
            animate={{
              rotate: 360,
              opacity: [0.05, 0.25, 0.05],
              scale: [0.8, 1.4, 0.8],
            }}
            transition={{
              duration: 80 + i * 20,
              repeat: Infinity,
              ease: "linear",
            }}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 min-h-screen flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.5 }}
          className="w-full max-w-5xl bg-black/70 backdrop-blur-3xl border border-cyan-400/20 rounded-3xl p-12 md:p-20 shadow-[0_0_80px_rgba(0,240,255,0.15)]"
        >
          <h1 className="text-6xl md:text-9xl font-black text-center mb-10 bg-gradient-to-r from-cyan-300 via-purple-400 to-pink-400 bg-clip-text text-transparent tracking-[0.15em] drop-shadow-[0_0_20px_rgba(0,240,255,0.6)]">
            BUILDER PROTOCOL
          </h1>

          <p className="text-center text-3xl text-cyan-200 mb-16 tracking-wide">
            2050–2100 Era Construction Intelligence
          </p>

          <div className="space-y-12">
            <div>
              <label className="block text-2xl font-bold mb-5 text-cyan-200 tracking-wider">PROJECT DESIGNATION</label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="e.g. Orbital Habitat Alpha-7"
                className="w-full p-7 bg-black/60 border border-cyan-400/30 rounded-2xl text-white text-2xl focus:outline-none focus:border-cyan-300 focus:ring-4 focus:ring-cyan-500/30 transition-all shadow-inner"
              />
            </div>

            <div>
              <label className="block text-2xl font-bold mb-5 text-cyan-200 tracking-wider">MISSION PARAMETERS</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Specify structure type, location, scale, materials, energy requirements..."
                rows={8}
                className="w-full p-7 bg-black/60 border border-cyan-400/30 rounded-2xl text-white text-2xl focus:outline-none focus:border-cyan-300 focus:ring-4 focus:ring-cyan-500/30 transition-all shadow-inner resize-none"
              />
            </div>

            <div className="text-center pt-10">
              <motion.button
                whileHover={{ scale: 1.08, boxShadow: '0 0 60px rgba(0,240,255,0.5)' }}
                whileTap={{ scale: 0.95 }}
                onClick={handleBuild}
                disabled={loading}
                className="px-24 py-10 bg-gradient-to-r from-cyan-600 via-purple-700 to-pink-700 hover:from-cyan-500 hover:via-purple-600 hover:to-pink-600 text-white text-3xl font-black rounded-3xl shadow-2xl transition-all duration-500 disabled:opacity-40"
              >
                {loading ? 'PROTOCOL EXECUTING...' : 'INITIATE QUANTUM BUILD'}
              </motion.button>
            </div>

            {error && <p className="text-red-400 text-center text-2xl mt-10 font-semibold">{error}</p>}

            {result && (
              <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-16 p-12 bg-black/80 border border-cyan-400/20 rounded-3xl shadow-[0_0_60px_rgba(0,240,255,0.2)]"
              >
                <h2 className="text-5xl font-black text-center mb-10 text-cyan-300 tracking-widest drop-shadow-lg">
                  GROK-2100 CONSTRUCTION PROTOCOL
                </h2>
                <pre className="text-cyan-100 text-2xl whitespace-pre-wrap font-mono leading-relaxed">
                  {result}
                </pre>
              </motion.div>
            )}
          </div>

          <p className="text-center mt-20 text-2xl text-gray-500">
            Free prototype session • One build per visitor
          </p>
        </motion.div>
      </div>
    </div>
  );
}
