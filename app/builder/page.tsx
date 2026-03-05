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
      setError('Please enter project name and description');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // === ITT JÖN MAJD A VALÓDI GROK API HÍVÁS ===
      // Később ezt cseréljük server action-re vagy API route-ra
      await new Promise(resolve => setTimeout(resolve, 2800));

      const aiResponse = `
PROJECT: ${projectName}

DESCRIPTION: ${description}

GROK AI BUILD PLAN (2050-2100 era simulation):

• Structural Analysis: 98.7% stability with quantum-reinforced composite materials
• Material Recommendation: 620 m³ self-healing nano-concrete + 24 tons carbon-nanotube steel
• Construction Timeline: 29 days (AI-optimized swarm robotics schedule)
• Energy Efficiency: +47% (integrated orbital solar array + zero-point energy prototype)
• Cost Estimation: $4.82M (with 12% AI cost optimization)
• Risk Factors: Low (weather 3%, supply chain 1%)
• Suggested Upgrades: Holographic interior walls, neural interface control system

This is a free demo build. Register to unlock unlimited builds and full AI collaboration.
      `;

      setResult(aiResponse.trim());
    } catch (err) {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black overflow-hidden relative">
      {/* 2050-2100 futuristic floating background elements */}
      <div className="absolute inset-0 pointer-events-none">
        {Array.from({ length: 8 }).map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-cyan-400 rounded-full blur-xl"
            initial={{
              x: Math.random() * 2000 - 500,
              y: Math.random() * 2000 - 500,
              opacity: 0.15,
            }}
            animate={{
              x: Math.random() * 2000 - 500,
              y: Math.random() * 2000 - 500,
              opacity: [0.15, 0.4, 0.15],
            }}
            transition={{
              duration: 25 + Math.random() * 30,
              repeat: Infinity,
              ease: "linear",
            }}
          />
        ))}
      </div>

      <div className="relative z-10 min-h-screen flex items-center justify-center p-6">
        <div className="w-full max-w-5xl bg-zinc-950/80 backdrop-blur-3xl border border-cyan-400/30 rounded-3xl p-12 md:p-20 shadow-2xl">
          <motion.h1
            initial={{ opacity: 0, y: -30 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-6xl md:text-8xl font-bold text-center mb-6 bg-gradient-to-r from-cyan-300 via-purple-400 to-pink-400 bg-clip-text text-transparent tracking-widest"
          >
            BUILDER PROTOCOL
          </motion.h1>

          <p className="text-center text-2xl text-cyan-200 mb-16">
            2050–2100 Era Construction Intelligence
          </p>

          <div className="space-y-10">
            <div>
              <label className="block text-xl font-semibold mb-4 text-cyan-300">PROJECT NAME</label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="e.g. Neo-Tokyo Arcology Tower"
                className="w-full p-6 bg-zinc-900 border border-cyan-400/30 rounded-2xl text-white text-xl focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/50 transition-all"
              />
            </div>

            <div>
              <label className="block text-xl font-semibold mb-4 text-cyan-300">PROJECT DESCRIPTION</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe the building, location, size, special requirements..."
                rows={7}
                className="w-full p-6 bg-zinc-900 border border-cyan-400/30 rounded-2xl text-white text-xl focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/50 transition-all resize-none"
              />
            </div>

            <div className="text-center pt-8">
              <button
                onClick={handleBuild}
                disabled={loading}
                className="px-20 py-8 bg-gradient-to-r from-cyan-500 via-purple-600 to-pink-600 hover:from-cyan-400 hover:via-purple-500 hover:to-pink-500 text-white text-3xl font-bold rounded-2xl shadow-2xl transform hover:scale-105 transition-all duration-300 disabled:opacity-50"
              >
                {loading ? 'GROK IS BUILDING...' : 'INITIATE CONSTRUCTION PROTOCOL'}
              </button>
            </div>

            {error && <p className="text-red-400 text-center text-xl mt-8">{error}</p>}

            {result && (
              <div className="mt-16 p-10 bg-black/70 border border-cyan-400/30 rounded-3xl">
                <h2 className="text-4xl font-bold text-cyan-300 mb-8 text-center">GROK AI CONSTRUCTION PLAN</h2>
                <pre className="text-gray-200 text-xl whitespace-pre-wrap font-mono leading-relaxed">
                  {result}
                </pre>
              </div>
            )}
          </div>

          <p className="text-center mt-20 text-xl text-gray-500">
            Free demo mode • 1 build without registration
          </p>
        </div>
      </div>
    </div>
  );
}
