"use client";

import { useState } from 'react';
import { supabase } from '@/lib/supabaseClient'; // importáld a te kliensedet
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

      // Automatikus profil létrejön a trigger miatt → mutassuk role választót
      setShowRoleSelect(true);
    } catch (err: any) {
      setError(err.message || 'Regisztrációs hiba');
    } finally {
      setLoading(false);
    }
  };

  const handleRoleSave = async () => {
    setLoading(true);
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Nincs user');

      const { error } = await supabase
        .from('profiles')
        .update({ role: selectedRole })
        .eq('id', user.id);

      if (error) throw error;

      router.push('/dashboard'); // vagy ahova akarod
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (showRoleSelect) {
    return (
      <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
        <h2 className="text-2xl mb-4">Válassz szerepkört</h2>
        <select
          value={selectedRole}
          onChange={(e) => setSelectedRole(e.target.value)}
          className="border p-2 mb-4 w-full"
        >
          <option value="manufacturer">Manufacturer</option>
          <option value="business_buyer">Business Buyer</option>
          <option value="individual_buyer">Individual Buyer</option>
          <option value="builder">Builder</option>
        </select>
        <button
          onClick={handleRoleSave}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded w-full"
        >
          {loading ? 'Mentés...' : 'Mentés és folytatás'}
        </button>
        {error && <p className="text-red-500 mt-2">{error}</p>}
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h1 className="text-3xl mb-6">Regisztráció</h1>
      <form onSubmit={handleSignup}>
        <input
          type="email"
          placeholder="Email cím"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 mb-4 w-full"
          required
        />
        <input
          type="password"
          placeholder="Jelszó"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 mb-4 w-full"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-green-600 text-white px-4 py-2 rounded w-full"
        >
          {loading ? 'Folyamatban...' : 'Regisztráció'}
        </button>
      </form>
      {error && <p className="text-red-500 mt-4">{error}</p>}
      <p className="mt-4 text-center">
        Már van fiókod? <a href="/login" className="text-blue-600">Bejelentkezés</a>
      </p>
    </div>
  );
}
