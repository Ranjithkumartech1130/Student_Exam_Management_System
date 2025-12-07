"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { studentLogin } from '../../services/api';

export default function StudentLogin() {
    const [regNo, setRegNo] = useState('');
    const [dob, setDob] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await studentLogin(regNo, dob);
            if (response.data.success) {
                localStorage.setItem('studentData', JSON.stringify(response.data.data));
                router.push('/student/dashboard');
            } else {
                setError(response.data.error || 'Login failed');
            }
        } catch (err) {
            setError('Login failed. Please check credentials.');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-black p-4">
            <div className="glass-panel p-8 rounded-2xl w-full max-w-md border-t border-purple-500/50">
                <h1 className="text-3xl font-bold mb-6 text-center text-white">Student Portal</h1>
                {error && <p className="text-red-400 mb-4 text-center text-sm">{error}</p>}
                <form onSubmit={handleLogin} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium mb-2 text-gray-400">Register Number</label>
                        <input
                            type="text"
                            value={regNo}
                            onChange={(e) => setRegNo(e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-lg p-3 text-white focus:ring-2 focus:ring-purple-500 uppercase"
                            placeholder="e.g. 24UAM139"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-2 text-gray-400">Date of Birth</label>
                        <input
                            type="date"
                            value={dob}
                            onChange={(e) => setDob(e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-lg p-3 text-white focus:ring-2 focus:ring-purple-500"
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-lg font-bold"
                    >
                        Check Seating
                    </button>
                </form>
            </div>
        </div>
    );
}
