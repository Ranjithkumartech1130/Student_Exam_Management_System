"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { login, studentLogin } from '../../services/api';

export default function AdminLogin() {
    const [activeTab, setActiveTab] = useState('admin'); // 'faculty' | 'student' | 'admin'
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const router = useRouter();

    // Inputs
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [regNo, setRegNo] = useState('');
    const [dob, setDob] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (activeTab === 'admin') {
                const res = await login(username, password);
                if (res.data.success) {
                    router.push('/admin/dashboard');
                } else {
                    setError('Invalid Admin Credentials');
                }
            }
            else if (activeTab === 'student') {
                const res = await studentLogin(regNo, dob);
                if (res.data.success) {
                    localStorage.setItem('studentData', JSON.stringify(res.data.data));
                    router.push('/student/dashboard');
                } else {
                    setError('Invalid Student Details');
                }
            }
            else if (activeTab === 'faculty') {
                // Placeholder for Faculty
                if (username === 'faculty' && password === 'admin') {
                    setError("Faculty Portal Coming Soon");
                } else {
                    setError('Invalid Faculty Credentials');
                }
            }
        } catch (err) {
            setError('Connection Failed');
        }
        setLoading(false);
    };

    return (
        <div className="min-h-screen flex items-center justify-center font-sans relative">

            {/* Background Image (Building) */}
            <div
                className="absolute inset-0 z-0 bg-cover bg-center"
                style={{
                    backgroundImage: "url('https://images.unsplash.com/photo-1562774053-701939374585?q=80&w=1986&auto=format&fit=crop')",
                    filter: "brightness(0.8)"
                }}
            ></div>

            {/* Glass Modal */}
            <div className="relative z-10 w-full max-w-md bg-white/10 backdrop-blur-md rounded-3xl border-2 border-indigo-600/50 shadow-2xl overflow-hidden p-8 text-center">

                {/* Title */}
                <h1 className="text-3xl font-bold text-indigo-900 mb-2 drop-shadow-md">
                    SinthanAI Login <br /> Portal
                </h1>

                {/* Tabs */}
                <div className="flex justify-center gap-2 my-6">
                    {['faculty', 'student', 'admin'].map((tab) => (
                        <button
                            key={tab}
                            onClick={() => { setActiveTab(tab); setError(''); }}
                            className={`
                 px-6 py-2 rounded-full text-sm font-bold capitalize transition-all border
                 ${activeTab === tab
                                    ? 'bg-white text-gray-800 border-white shadow-lg scale-105'
                                    : 'bg-transparent text-white border-white/50 hover:bg-white/10'
                                }
               `}
                        >
                            {tab}
                        </button>
                    ))}
                </div>

                {/* Dynamic Heading */}
                <h2 className="text-white text-lg font-medium mb-6 capitalize drop-shadow-md">
                    {activeTab} Login
                </h2>

                {/* Form */}
                <form onSubmit={handleLogin} className="flex flex-col gap-4">

                    {error && <div className="bg-red-500/80 text-white text-xs p-2 rounded-lg">{error}</div>}

                    {activeTab === 'student' ? (
                        <>
                            <input
                                type="text"
                                placeholder="Register Number"
                                className="w-full py-3 px-4 rounded-xl bg-white/90 border-none text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-indigo-500 outline-none text-center shadow-inner"
                                value={regNo}
                                onChange={e => setRegNo(e.target.value)}
                                required
                            />
                            <input
                                type="date"
                                className="w-full py-3 px-4 rounded-xl bg-white/90 border-none text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-indigo-500 outline-none text-center shadow-inner"
                                value={dob}
                                onChange={e => setDob(e.target.value)}
                                required
                            />
                        </>
                    ) : (
                        <>
                            <input
                                type="text"
                                placeholder={activeTab === 'admin' ? "Admin Username" : "Faculty ID"}
                                className="w-full py-3 px-4 rounded-xl bg-white/90 border-none text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-indigo-500 outline-none text-center shadow-inner"
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                                required
                            />
                            <input
                                type="password"
                                placeholder="Password"
                                className="w-full py-3 px-4 rounded-xl bg-white/90 border-none text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-indigo-500 outline-none text-center shadow-inner"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                required
                            />
                        </>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="mt-4 w-full py-3 rounded-xl bg-white text-gray-900 font-bold hover:bg-gray-100 transition-all shadow-lg active:scale-95 flex justify-center items-center"
                    >
                        {loading ? "Verifying..." : "Login"}
                    </button>
                </form>

            </div>
        </div>
    );
}
