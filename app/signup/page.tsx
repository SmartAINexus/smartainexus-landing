"use client";

import { createClient } from '@supabase/supabase-js';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export const dynamic = 'force-dynamic';

export default function SignupPage() {
  const [supabase, setSupabase] = useState<any>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showRoleSelect, setShowRoleSelect] = useState(false);
  const [selectedRole, setSelectedRole] = useState('individual_buyer');
  const router = useRouter();

  useEffect(() => {
    const client = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
    );
    setSupabase(client);
  }, []);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!supabase) return;
    setLoading(true);
    setError(null);

    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          emailRedirectTo: window.location.origin + '/', 
        },
      });

      if (error) throw error;

      if (data.session) {
        await supabase.auth.setSession(data.session);
        setShowRoleSelect(true);
      } else {
        const { error: signInError } = await supabase.auth.signInWithPassword({
          email,
          password,
        });
        if (signInError) throw signInError;
        setShowRoleSelect(true);
      }
    } catch (err: any) {
      setError(err.message || 'Hiba a regisztráció során');
    } finally {
      setLoading(false);
    }
  };

  const handleRoleSave = async () => {
    if (!supabase) return;
    setLoading(true);
    setError(null);

    try {
      const { error: refreshError } = await supabase.auth.refreshSession();
      if (refreshError) throw refreshError;

      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Nincs bejelentkezve – próbáld újra');

      const { error } = await supabase
        .from('profiles')
        .update({ role: selectedRole })
        .eq('id', user.id);

      if (error) throw error;

      router.push('/');
    } catch (err: any) {
      setError(err.message || 'Hiba a role mentésekor');
    } finally {
      setLoading(false);
    }
  };

  if (!supabase) {
    return <div className="min-h-screen flex items-center justify-center">Betöltés...</div>;
  }

  if (showRoleSelect) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
        <div className="max-w-md w-full bg-white p-8 rounded-2xl shadow">
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
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-lg font-semibold text-lg"
          >
            {loading ? 'Mentés...' : 'Mentés és folytatás'}
          </button>
          {error && <p className="text-red-500 text-center mt-4">{error}</p>}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="max-w-md w-full bg-white p-8 rounded-2xl shadow">
        <h1 className="text-4xl font-bold text-center mb-8">Regisztráció</h1>
        <form onSubmit={handleSignup} className="space-y-4">
          <input
            type="email"
            placeholder="Email cím"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-4 border border-gray-300 rounded-lg text-lg"
            required
          />
          <input
            type="password"
            placeholder="Jelszó"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-4 border border-gray-300 rounded-lg text-lg"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 text-white py-4 rounded-lg font-semibold text-lg"
          >
            {loading ? 'Regisztráció folyamatban...' : 'Regisztráció'}
          </button>
        </form>
        {error && <p className="text-red-500 text-center mt-4">{error}</p>}
      </div>
    </div>
  );
}
