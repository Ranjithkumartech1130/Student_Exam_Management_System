"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function StudentDashboard() {
    const [student, setStudent] = useState(null);
    const router = useRouter();

    useEffect(() => {
        const data = localStorage.getItem('studentData');
        if (data) {
            setStudent(JSON.parse(data));
        } else {
            router.push('/student/login');
        }
    }, [router]);

    if (!student) return <div className="text-white text-center mt-20">Loading...</div>;

    return (
        <div className="min-h-screen bg-black text-white p-6 flex flex-col items-center">
            <div className="w-full max-w-2xl">
                <h1 className="text-3xl font-bold mb-8 gradient-text text-center">Exam Hall Ticket</h1>

                <div className="glass-panel p-8 rounded-3xl relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-purple-500 to-pink-500"></div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        <div>
                            <div className="text-gray-400 text-sm">Register Number</div>
                            <div className="text-2xl font-mono font-bold text-white">{student.register_no}</div>
                        </div>
                        <div>
                            <div className="text-gray-400 text-sm">Name</div>
                            <div className="text-xl font-bold text-white">{student.student_name}</div>
                        </div>
                    </div>

                    <div className="border-t border-gray-800 my-6"></div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-white/5 p-4 rounded-xl">
                            <div className="text-gray-400 text-xs">Allocated Room</div>
                            <div className="text-3xl font-bold text-green-400">{student.exam_hall_number || "Not Assigned"}</div>
                        </div>
                        <div className="bg-white/5 p-4 rounded-xl">
                            <div className="text-gray-400 text-xs">Seat Number</div>
                            <div className="text-3xl font-bold text-yellow-400">{student.exam_seat_number || "Wait"}</div>
                        </div>
                    </div>

                    <div className="mt-8 grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span className="text-gray-500">Course:</span> <br />
                            <span className="text-gray-300">{student.course_code} - {student.course_title}</span>
                        </div>
                        <div>
                            <span className="text-gray-500">Time:</span> <br />
                            <span className="text-gray-300">{student.exam_date} ({student.exam_session})</span>
                        </div>
                    </div>
                </div>

                <button
                    onClick={() => {
                        localStorage.removeItem('studentData');
                        router.push('/');
                    }}
                    className="mt-8 w-full text-gray-500 hover:text-white transition-colors"
                >
                    Logout
                </button>
            </div>
        </div>
    );
}
