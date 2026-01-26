import React, { useEffect, useState } from 'react';
import { checkHealth } from '../services/api';
import { HardDrive, CheckCircle2, AlertCircle } from 'lucide-react';

const Home = () => {
    const [status, setStatus] = useState("checking");

    useEffect(() => {
        checkHealth().then(res => {
            if (res.message) setStatus("online");
            else setStatus("offline");
        }).catch(() => setStatus("offline"));
    }, []);

    return (
        <div className="space-y-4">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-slate-900">Gerador de Propostas</h1>
                <p className="text-slate-500 mt-2">Crie propostas técnicas complexas com auxílio de IA.</p>
            </header>

            {/* Status Card */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                    <div>
                        <p className="text-sm font-medium text-slate-500">Status da API</p>
                        <div className="flex items-center gap-2 mt-1">
                            {status === "online" ? (
                                <>
                                    <h3 className="text-2xl font-bold text-green-600">Online</h3>
                                    <CheckCircle2 size={20} className="text-green-500" />
                                </>
                            ) : (
                                <>
                                    <h3 className="text-2xl font-bold text-red-600">Offline</h3>
                                    <AlertCircle size={20} className="text-red-500" />
                                </>
                            )}
                        </div>
                    </div>
                    <div className="p-3 bg-slate-50 rounded-lg">
                        <HardDrive className="text-slate-400" size={24} />
                    </div>
                </div>
            </div>

            <div className="mt-8 bg-white rounded-xl border border-slate-200 p-8 text-center ring-1 ring-slate-900/5">
                <h2 className="text-xl font-semibold mb-2">Pronto para começar?</h2>
                <p className="text-slate-500 mb-6">Utilize o formulário para gerar uma nova proposta do zero.</p>
                <div className="inline-flex gap-4">
                    {/* Placeholder form area */}
                </div>
            </div>
        </div>
    );
};

export default Home;
