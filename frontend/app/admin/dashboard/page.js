"use client";
import { useState, useEffect } from 'react';
import { getRooms, toggleRoom, uploadCSV, generateSeating } from '../../services/api';

export default function AdminDashboard() {
    const [rooms, setRooms] = useState([]);
    const [file, setFile] = useState(null);
    const [allocation, setAllocation] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [newRoom, setNewRoom] = useState({ number: '', capacity: '' });
    const [selectedFloor, setSelectedFloor] = useState(null);

    useEffect(() => {
        fetchRooms();
    }, []);

    const fetchRooms = async () => {
        try {
            const res = await getRooms();
            if (res.data.success) setRooms(res.data.data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleToggleRoom = async (id) => {
        await toggleRoom(id);
        fetchRooms();
    };

    const handleUpload = async () => {
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);
        setLoading(true);
        try {
            const res = await uploadCSV(formData);
            setMessage(res.data.message || 'Upload successful');
        } catch (err) {
            setMessage('Upload failed');
        }
        setLoading(false);
    };

    const handleGenerate = async () => {
        setLoading(true);
        try {
            const res = await generateSeating();
            if (res.data.success) {
                setAllocation(res.data.data);
                setMessage(res.data.message);
            } else {
                setMessage(res.data.error || 'Generation failed');
            }
        } catch (err) {
            setMessage('Error allocating seats');
        }
        setLoading(false);
    };

    const handleRefresh = async () => {
        if (!confirm('This will clear all existing allocations and regenerate new ones. Continue?')) return;

        setLoading(true);
        try {
            const { refreshAllocation } = await import('../../services/api');
            const res = await refreshAllocation();
            if (res.data.success) {
                setAllocation(res.data.data);
                setMessage(res.data.message);
            } else {
                setMessage(res.data.error || 'Refresh failed');
            }
        } catch (err) {
            setMessage('Error refreshing allocations');
        }
        setLoading(false);
    };

    const handleAddRoom = async (e) => {
        e.preventDefault();
        if (!newRoom.number || !newRoom.capacity) return;

        try {
            const res = await import('../../services/api').then(mod => mod.addRoom(newRoom.number, newRoom.capacity));
            if (res.data.success) {
                setNewRoom({ number: '', capacity: '' });
                fetchRooms();
                setMessage('Room added successfully');
            } else {
                setMessage(res.data.error || 'Failed to add room');
            }
        } catch (err) {
            setMessage('Error adding room');
        }
    };

    // Group rooms by floor (first digit)
    const floors = [...new Set(rooms.map(r => r.room_number.charAt(0)))].sort();

    const getRoomsByFloor = (floor) => {
        return rooms.filter(r => r.room_number.startsWith(floor));
    };

    const countSelected = (floor) => {
        return getRoomsByFloor(floor).filter(r => r.is_available).length;
    }

    return (
        <div className="min-h-screen bg-slate-100 text-slate-900 font-sans">
            {/* Header */}
            <div className="bg-slate-900 text-white p-4 text-center font-bold text-lg tracking-wider uppercase shadow-lg">
                Halls
            </div>

            <div className="max-w-md mx-auto p-6">

                {/* View 1: Floor Selection */}
                {!selectedFloor ? (
                    <div className="flex flex-col gap-4">
                        <div className="text-center mb-6">
                            <h2 className="text-2xl font-bold text-slate-800">Which floor?</h2>
                        </div>
                        {floors.map(floor => (
                            <button
                                key={floor}
                                onClick={() => setSelectedFloor(floor)}
                                className="bg-white hover:bg-slate-50 text-slate-800 font-bold py-4 px-6 rounded-2xl shadow-sm border border-slate-200 text-lg transition-transform active:scale-95 flex justify-between items-center"
                            >
                                <span>Floor {floor}</span>
                                <span className="text-xs bg-slate-200 px-2 py-1 rounded-full text-slate-600">
                                    {countSelected(floor)} Selected
                                </span>
                            </button>
                        ))}
                        {rooms.length === 0 && (
                            <div className="text-center text-gray-500 py-10">
                                No rooms found. Add some using the "Add Room" form below.
                            </div>
                        )}

                        {/* Temporary Admin Tools (Hidden/Miniaturized) */}
                        <div className="mt-8 border-t pt-8">
                            <h3 className="text-sm font-bold text-gray-400 mb-2 uppercase">Admin Controls</h3>
                            <form onSubmit={handleAddRoom} className="flex gap-2 mb-4">
                                <input placeholder="Room (e.g. 101)" value={newRoom.number} onChange={e => setNewRoom({ ...newRoom, number: e.target.value })} className="border p-2 rounded w-full" />
                                <input placeholder="Cap" type="number" value={newRoom.capacity} onChange={e => setNewRoom({ ...newRoom, capacity: e.target.value })} className="border p-2 rounded w-20" />
                                <button className="bg-blue-600 text-white px-4 rounded">Add</button>
                            </form>
                            <button onClick={() => document.getElementById('uploader').click()} className="text-blue-600 text-sm font-bold bg-blue-50 px-4 py-2 rounded-lg w-full mb-2">
                                Upload Student CSV
                            </button>
                            <input id="uploader" type="file" hidden accept=".csv" onChange={(e) => { setFile(e.target.files[0]); handleUpload(); }} />

                            <button onClick={handleGenerate} className="bg-slate-900 text-white w-full py-3 rounded-xl font-bold shadow-lg">
                                {loading ? 'Generating...' : 'Generate Seating Plan'}
                            </button>
                            <button onClick={handleRefresh} className="bg-amber-600 hover:bg-amber-700 text-white w-full py-3 rounded-xl font-bold shadow-lg mt-2 transition-colors">
                                {loading ? 'Refreshing...' : '🔄 Refresh Allocation'}
                            </button>
                            {message && <div className="text-center text-green-600 mt-2 font-bold">{message}</div>}
                        </div>

                        {/* Results Section */}
                        {allocation && (
                            <div className="mt-8 bg-white p-4 rounded-xl shadow-sm border">
                                <h3 className="font-bold mb-2">Seating Plan Preview</h3>
                                <div className="text-sm text-gray-600 mb-2">Total: {allocation.total_allocated} students</div>
                                <div className="max-h-60 overflow-y-auto font-mono text-xs">
                                    {allocation.allocations.slice(0, 50).map((a, i) => (
                                        <div key={i} className="border-b py-1 flex justify-between">
                                            <span>{a.room}</span>
                                            <span>{a.register_no}</span>
                                        </div>
                                    ))}
                                    {allocation.allocations.length > 50 && <div className="text-center py-2 text-gray-400">...and more</div>}
                                </div>
                            </div>
                        )}
                    </div>
                ) : (
                    /* View 2: Room Grid */
                    <div>
                        <div className="flex items-center mb-6 relative">
                            <button
                                onClick={() => setSelectedFloor(null)}
                                className="absolute left-0 text-slate-400 hover:text-slate-800 p-2"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-6 h-6">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
                                </svg>
                            </button>
                            <div className="w-full text-center">
                                <h2 className="text-2xl font-bold text-slate-800">Floor {selectedFloor}</h2>
                                <p className="text-xs text-slate-500 font-bold uppercase tracking-widest">{countSelected(selectedFloor)} Selected</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            {getRoomsByFloor(selectedFloor).map(room => (
                                <button
                                    key={room.id}
                                    onClick={() => handleToggleRoom(room.id)}
                                    className={`
                                        relative group p-6 rounded-2xl font-bold text-xl transition-all shadow-sm border
                                        flex flex-col items-center justify-center min-h-[120px]
                                        ${room.is_available
                                            ? 'bg-slate-900 text-white border-slate-900'
                                            : 'bg-white text-slate-800 border-slate-200 hover:border-slate-300'
                                        }
                                    `}
                                >
                                    <span>{room.room_number}</span>

                                    {/* Checkmark Circle */}
                                    {room.is_available && (
                                        <div className="mt-2 text-green-400">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
                                                <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clipRule="evenodd" />
                                            </svg>
                                        </div>
                                    )}
                                </button>
                            ))}
                        </div>

                        <div className="fixed bottom-0 left-0 w-full bg-white p-4 border-t shadow-[0_-5px_20px_rgba(0,0,0,0.05)]">
                            <div className="max-w-md mx-auto flex justify-between items-center">
                                <span className="text-slate-500 font-medium">Block {countSelected(selectedFloor)} halls?</span>
                                <button onClick={() => setSelectedFloor(null)} className="bg-slate-900 text-white px-8 py-3 rounded-xl font-bold">
                                    OK
                                </button>
                            </div>
                        </div>
                        <div className="h-24"></div> {/* Spacer for fixed footer */}
                    </div>
                )}
            </div>
        </div>
    );
}
