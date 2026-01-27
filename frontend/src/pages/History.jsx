import React, { useEffect, useState } from 'react';
import { getHistory } from '../services/api';

const History = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getHistory()
            .then(data => setHistory(data))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="space-y-6">
            <header>
                <h1 className="text-3xl font-bold text-neutral-dark">Histórico de Propostas</h1>
                <p className="text-neutral-gray">Visualize as propostas geradas anteriormente.</p>
            </header>

            {loading ? (
                <div className="flex items-center gap-2 text-neutral-gray">
                    <span className="material-symbols-outlined animate-spin">progress_activity</span>
                    <span>Carregando histórico...</span>
                </div>
            ) : history.length === 0 ? (
                <div className="p-8 bg-white border border-surface-light rounded-xl text-center text-neutral-gray">
                    Nenhuma proposta encontrada.
                </div>
            ) : (
                <div className="grid gap-4">
                    {history.map((item) => (
                        <div key={item.timestamp} className="bg-white p-6 rounded-xl border border-surface-light shadow-sm hover:shadow-md transition-shadow">
                            <div className="flex items-center justify-between mb-4">
                                <div className="flex items-center gap-2 text-neutral-gray text-sm">
                                    <span className="material-symbols-outlined text-sm">calendar_today</span>
                                    <span>{item.timestamp.split('_')[0]}</span>
                                    <span className="material-symbols-outlined text-sm ml-2">schedule</span>
                                    <span>{item.timestamp.split('_')[1].replace(/-/g, ':')}</span>
                                </div>
                                <span className="bg-blue-50 text-primary text-xs px-2 py-1 rounded-full font-bold">Completed</span>
                            </div>

                            <h3 className="font-bold text-lg text-neutral-dark mb-2">Proposta {item.timestamp}</h3>

                            <div className="space-y-1">
                                {item.files.filter(f => f.endsWith('.md') && !f.startsWith('MAT_') && !f.startsWith('MOD_')).map(file => (
                                    <div key={file} className="flex items-center gap-2 text-sm text-neutral-gray group">
                                        <span className="material-symbols-outlined text-sm text-primary">description</span>
                                        <a href={`http://localhost:8000/output/${item.timestamp}/${file}`} target="_blank" rel="noopener noreferrer" className="hover:text-primary hover:underline transition-colors">
                                            {file}
                                        </a>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default History;
