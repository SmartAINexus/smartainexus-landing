"use client";

import { useState } from 'react';
import { supabase } from '../../lib/supabaseClient';   // ← relatív import (biztonságos Vercelen)
import { useRouter } from 'next/navigation';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showRoleSelect, setShowRoleSelect] = useState(false);
  const [selectedRole, setSelectedRole] = useState('individual_buyer');
  const router = useRouter();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const { error } = await supabase.auth.signUp({ email, password });
      if (error) throw error;
      setShowRoleSelect(true); // trigger miatt már van profil
    } catch (err: any) {
      setError(err.message || 'Regisztrációs hiba történt');
    } finally {
      setLoading(false);
    }
  };

  const handleRoleSave = async () => {
    setLoading(true);
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Nincs bejelentkezve');

      const { error } = await supabase
        .from('profiles')
        .update({ role: selectedRole })
        .eq('id', user.id);

      if (error) throw error;

      router.push('/dashboard'); // később létrehozhatod
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Role választó képernyő
  if (showRoleSelect) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white p-8 rounded-xl shadow">
          <h2 className="text-3xl font-bold text-center mb-6">Válassz szerepkört</h2>
          <select
            value={selectedRole}
            onChange={(e) => setSelectedRole(e.target.value)}
            className="w-full border border-gray-300 p-3 rounded-lg mb-6 text-lg"
          >
            <option value="manufacturer">Gyártó (Manufacturer)</option>
            <option value="business_buyer">Üzleti vevő (Business Buyer)</option>
            <option value="individual_buyer">Magánvevő (Individual Buyer)</option>
            <option value="builder">Építő (Builder)</option>
          </select>
          <button
            onClick={handleRoleSave}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 rounded-lg text-lg transition"
          >
            {loading ? 'Mentés...' : 'Mentés és belépés'}
          </button>
          {error && <p className="text-red-500 text-center mt-4">{error}</p>}
        </div>
      </div>
    );
  }

  // Regisztrációs űrlap
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded-xl shadow">
        <h1 className="text-4xl font-bold text-center mb-8">Regisztráció</h1>
        <form onSubmit={handleSignup}>
          <input
            type="email"
            placeholder="Email cím"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border border-gray-300 p-4 rounded-lg mb-4 text-lg"
            required
          />
          <input
            type="password"
            placeholder="Jelszó"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border border-gray-300 p-4 rounded-lg mb-6 text-lg"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-4 rounded-lg text-lg transition"
          >
            {loading ? 'Regisztráció folyamatban...' : 'Regisztráció'}
          </button>
        </form>
        {error && <p className="text-red-500 text-center mt-4">{error}</p>}
        <p className="text-center mt-6 text-gray-600">
          Már van fiókod?{' '}
          <a href="/login" className="text-blue-600 font-medium hover:underline">
            Bejelentkezés
          </a>
        </p>
      </div>
    </div>
  );
}
