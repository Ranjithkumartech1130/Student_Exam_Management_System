"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { login, studentLogin } from './services/api';

export default function Home() {
  const [role, setRole] = useState('student'); // 'student' | 'faculty' | 'admin'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  // Admin/Faculty State
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Student State
  const [regNo, setRegNo] = useState('');
  const [dob, setDob] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (role === 'admin') {
        const res = await login(username, password);
        if (res.data.success) {
          router.push('/admin/dashboard');
        } else {
          setError(res.data.error || 'Invalid Admin Credentials');
        }
      }
      else if (role === 'student') {
        const res = await studentLogin(regNo, dob);
        if (res.data.success) {
          localStorage.setItem('studentData', JSON.stringify(res.data.data));
          router.push('/student/dashboard');
        } else {
          setError(res.data.error || 'Invalid Student Details');
        }
      }
      else if (role === 'faculty') {
        // Reuse Admin Login for now, or placeholder
        // Assuming faculty uses same user table for this demo
        const res = await login(username, password);
        if (res.data.success) {
          // In a real app, we'd check groups/roles here
          // For now, redirect to a placeholder faculty page
          setError("Faculty Portal Under Construction (Try Admin)");
        } else {
          setError('Invalid Faculty Credentials');
        }
      }
    } catch (err) {
      setError('Login Connection Failed');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4 font-sans relative overflow-hidden">

      {/* Background Decor */}
      <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] bg-blue-600/20 rounded-full blur-[100px]"></div>
      <div className="absolute bottom-[-20%] left-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[100px]"></div>

      <div className="w-full max-w-4xl bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl overflow-hidden flex flex-col md:flex-row z-10 border border-white/20">

        {/* Left Side: Illustration / Branding */}
        <div className="md:w-1/2 p-10 bg-gradient-to-br from-blue-900 to-slate-900 text-white flex flex-col justify-between relative">
          <div>
            <div className="h-2 w-16 bg-blue-500 rounded mb-6"></div>
            <h1 className="text-4xl font-bold mb-4">Exam <br />Portal</h1>
            <p className="text-blue-200 text-sm leading-relaxed">
              Seamlessly manage exams, generate seating arrangements, and view hall tickets with our advanced management system.
            </p>
          </div>

          <div className="mt-10">
            <div className="flex gap-3 mb-2">
              <div className="w-3 h-3 rounded-full bg-red-400"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
              <div className="w-3 h-3 rounded-full bg-green-400"></div>
            </div>
            <div className="bg-white/10 p-4 rounded-xl border border-white/5 backdrop-blur-sm text-xs font-mono text-blue-100">
              System.status = "Online";<br />
              Security.level = "Maximum";
            </div>
          </div>
        </div>

        {/* Right Side: Login Form */}
        <div className="md:w-1/2 p-10 bg-white">

          {/* Tabs */}
          <div className="flex gap-2 p-1 bg-slate-100 rounded-xl mb-8">
            {['student', 'faculty', 'admin'].map((r) => (
              <button
                key={r}
                onClick={() => { setRole(r); setError(''); }}
                className={`flex-1 py-2 text-sm font-bold rounded-lg capitalize transition-all ${role === r
                    ? 'bg-white text-slate-900 shadow-sm'
                    : 'text-slate-400 hover:text-slate-600'
                  }`}
              >
                {r}
              </button>
            ))}
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-bold text-slate-800 capitalize">
              {role} Login
            </h2>
            <p className="text-slate-400 text-xs mt-1">
              Enter your credentials to access the portal.
            </p>
          </div>

          {error && <div className="bg-red-50 text-red-500 text-xs p-3 rounded-lg mb-4">{error}</div>}

          <form onSubmit={handleLogin} className="flex flex-col gap-4">

            {role === 'student' ? (
              <>
                <div>
                  <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Register No</label>
                  <input
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 text-slate-800 focus:ring-2 focus:ring-blue-500 outline-none transition-all font-mono"
                    placeholder="e.g. 24UAM139"
                    value={regNo}
                    onChange={e => setRegNo(e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Date of Birth</label>
                  <input
                    type="date"
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 text-slate-800 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                    value={dob}
                    onChange={e => setDob(e.target.value)}
                  />
                </div>
              </>
            ) : (
              <>
                {/* Faculty & Admin Fields */}
                <div>
                  <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Username</label>
                  <input
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 text-slate-800 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                    placeholder={role === 'admin' ? "Admin Username" : "Faculty ID"}
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Password</label>
                  <input
                    type="password"
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 text-slate-800 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                    placeholder="••••••••"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                  />
                </div>
              </>
            )}

            <button
              disabled={loading}
              className="mt-4 w-full bg-slate-900 text-white py-3 rounded-xl font-bold hover:bg-slate-800 transition-all flex justify-center items-center"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              ) : (
                "Login to Portal"
              )}
            </button>

          </form>

        </div>
      </div>
    </div>
  );
}
