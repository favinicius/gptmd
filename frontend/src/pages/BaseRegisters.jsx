import React, { useState, useEffect } from 'react';
import { getHardware, getRoles, getActivities, getLogistics, createHardware, updateHardware } from '../services/api';

const Tabs = ({ activeTab, onTabChange }) => (
    <div className="flex border-b border-slate-700 mb-6">
        <button
            className={`px-6 py-2 font-medium transition-colors ${activeTab === 'mat' ? 'text-indigo-400 border-b-2 border-indigo-500' : 'text-slate-400 hover:text-slate-200'}`}
            onClick={() => onTabChange('mat')}
        >
            Materiais (MAT)
        </button>
        <button
            className={`px-6 py-2 font-medium transition-colors ${activeTab === 'mod' ? 'text-indigo-400 border-b-2 border-indigo-500' : 'text-slate-400 hover:text-slate-200'}`}
            onClick={() => onTabChange('mod')}
        >
            Mão de Obra (MOD)
        </button>
        <button
            className={`px-6 py-2 font-medium transition-colors ${activeTab === 'div' ? 'text-indigo-400 border-b-2 border-indigo-500' : 'text-slate-400 hover:text-slate-200'}`}
            onClick={() => onTabChange('div')}
        >
            Logística (DIV)
        </button>
    </div>
);

const HardwareTab = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');

    useEffect(() => {
        loadData();
    }, [search]);

    const loadData = async () => {
        try {
            setLoading(true);
            const data = await getHardware({ search: search, limit: 20 }); // Limit for performance
            setItems(data);
        } catch (error) {
            console.error("Failed to load hardware", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="flex justify-between mb-4">
                <input
                    type="text"
                    placeholder="Buscar hardware..."
                    className="w-1/3 p-2 bg-slate-900 border border-slate-700 rounded text-slate-200 focus:outline-none focus:border-indigo-500"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
                <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded shadow-lg flex items-center gap-2">
                    <span className="material-symbols-outlined">add</span>
                    Novo Item
                </button>
            </div>

            <div className="bg-slate-800 rounded-lg overflow-hidden border border-slate-700">
                <table className="w-full text-left bg-slate-800">
                    <thead className="bg-slate-900 text-slate-400 uppercase text-xs">
                        <tr>
                            <th className="p-3">Part Number</th>
                            <th className="p-3">Descrição</th>
                            <th className="p-3 text-right">Custo Lista</th>
                            <th className="p-3 text-center">Ações</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700">
                        {loading ? (
                            <tr><td colSpan="4" className="p-4 text-center text-slate-500">Carregando...</td></tr>
                        ) : items.length === 0 ? (
                            <tr><td colSpan="4" className="p-4 text-center text-slate-500">Nenhum item encontrado.</td></tr>
                        ) : (
                            items.map(item => (
                                <tr key={item.id} className="hover:bg-slate-750 transition-colors">
                                    <td className="p-3 text-slate-300 font-mono text-sm">{item.partnumber}</td>
                                    <td className="p-3 text-slate-300">
                                        <div className="font-medium">{item.description_base}</div>
                                        <div className="text-xs text-slate-500 truncate max-w-md">{item.description_detail}</div>
                                    </td>
                                    <td className="p-3 text-right text-emerald-400">
                                        {item.cost_list.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                                    </td>
                                    <td className="p-3 text-center">
                                        <button className="text-slate-400 hover:text-indigo-400">
                                            <span className="material-symbols-outlined">edit</span>
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

const LaborTab = () => {
    const [roles, setRoles] = useState([]);
    const [activities, setActivities] = useState([]);

    useEffect(() => {
        getRoles().then(setRoles);
        getActivities({ limit: 30 }).then(setActivities);
    }, []);

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1 bg-slate-800 p-4 rounded-lg border border-slate-700 h-fit">
                <h3 className="text-lg font-bold text-white mb-4 border-b border-slate-700 pb-2">Perfis Profissionais</h3>
                <ul className="space-y-2">
                    {roles.map(role => (
                        <li key={role.id} className="flex justify-between items-center p-2 bg-slate-900 rounded">
                            <span className="text-slate-300">{role.role}</span>
                            <span className="text-emerald-400 font-mono">R$ {role.cost_unit}/h</span>
                        </li>
                    ))}
                </ul>
            </div>

            <div className="lg:col-span-2 bg-slate-800 p-4 rounded-lg border border-slate-700">
                <h3 className="text-lg font-bold text-white mb-4 border-b border-slate-700 pb-2">Biblioteca de Atividades</h3>
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead className="bg-slate-900 text-slate-400 text-xs uppercase">
                            <tr>
                                <th className="p-2">ID</th>
                                <th className="p-2">Atividade</th>
                                <th className="p-2">Role</th>
                                <th className="p-2">Horas</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-700 text-sm">
                            {activities.map((act, i) => (
                                <tr key={i} className="hover:bg-slate-750">
                                    <td className="p-2 font-mono text-slate-500">{act.id}</td>
                                    <td className="p-2 text-slate-300">{act.name}</td>
                                    <td className="p-2 text-indigo-300">{act.role}</td>
                                    <td className="p-2 text-slate-400">{act.unit_hours}h</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

const LogisticsTab = () => {
    const [items, setItems] = useState([]);

    useEffect(() => {
        getLogistics().then(setItems);
    }, []);

    return (
        <div className="bg-slate-800 rounded-lg overflow-hidden border border-slate-700">
            <table className="w-full text-left">
                <thead className="bg-slate-900 text-slate-400 uppercase text-xs">
                    <tr>
                        <th className="p-3">Categoria</th>
                        <th className="p-3">Item</th>
                        <th className="p-3">Descrição</th>
                        <th className="p-3 text-right">Valor Est.</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-700">
                    {items.map(item => (
                        <tr key={item.id} className="hover:bg-slate-750">
                            <td className="p-3 text-xs uppercase tracking-wider text-slate-500">{item.category}</td>
                            <td className="p-3 font-mono text-indigo-400">{item.item_key}</td>
                            <td className="p-3 text-slate-300">{item.description}</td>
                            <td className="p-3 text-right text-emerald-400">
                                {item.cost_value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const BaseRegisters = () => {
    const [activeTab, setActiveTab] = useState('mat');

    return (
        <div className="max-w-7xl mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
                        Cadastro de Base
                    </h1>
                    <p className="text-slate-400 mt-1">Gestão centralizada de itens, preços e parâmetros globais.</p>
                </div>
            </div>

            <Tabs activeTab={activeTab} onTabChange={setActiveTab} />

            <div className="min-h-[500px]">
                {activeTab === 'mat' && <HardwareTab />}
                {activeTab === 'mod' && <LaborTab />}
                {activeTab === 'div' && <LogisticsTab />}
            </div>
        </div>
    );
};

export default BaseRegisters;
