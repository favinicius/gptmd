import React, { useState, useEffect } from 'react';
import { Button, Input, Select } from '../../ui';
import { calculatePricing } from '../../../services/api';

export const PricingDashboard = ({ onNext, onBack, initialData, intent, logisticsPlan }) => {
    const [loading, setLoading] = useState(false);
    const [proposalData, setProposalData] = useState(initialData || null);

    // Initial calculation if no data exists
    useEffect(() => {
        if (!proposalData && intent) {
            handleCalculate();
        }
    }, [intent]); // Added intent as dependency, removed proposalData from dependency to avoid loop if it was there (it wasn't but safe measure)

    const handleCalculate = async () => {
        setLoading(true);
        try {
            // Merge logistics plan into intent if needed or handle separately
            // For now, we assume the backend re-calculates based on stored intent + overrides
            // In a real scenario, we might need to update the intent with logistics data before sending
            const updatedIntent = { ...intent, logistics_override: logisticsPlan };
            const result = await calculatePricing(updatedIntent);
            setProposalData(result);
        } catch (error) {
            console.error(error);
            // Fallback for dev/mock if API fails
            console.log("Mocking pricing data due to error");
            setProposalData({
                total_capex: 150000.00,
                monthly_payment: 15000.00,
                total_materials: 120000.00,
                total_labor: 20000.00,
                total_services: 10000.00,
                summary: { margin_percent: 0.15 },
                materials_table: [
                    { item: "Switch Core Mock", qty: 2, total_price: 20000.00 },
                    { item: "AP Wi-Fi 6 Mock", qty: 10, total_price: 15000.00 }
                ],
                labor_table: [
                    { role: "Analista Sênior", hours: 40, total_price: 10000.00 }
                ],
                services_table: [
                    { service_name: "Instalação Física", total_price: 5000.00 }
                ]
            });
        } finally {
            setLoading(false);
        }
    };

    const formatCurrency = (val) => {
        if (typeof val !== 'number') return 'R$ 0,00';
        return val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    };

    if (!proposalData && loading) {
        return (
            <div className="flex flex-col items-center justify-center p-12 space-y-4 animate-fade-in">
                <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
                <p className="text-neutral-gray font-medium">Calculando custos detalhados...</p>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="bg-white p-6 rounded-xl border border-surface-light shadow-sm">
                <div className="flex justify-between items-center mb-6">
                    <div className="flex items-center gap-3">
                        <span className="material-symbols-outlined text-primary">attach_money</span>
                        <h3 className="text-lg font-bold text-neutral-dark">3. Dashboard Financeiro</h3>
                    </div>
                    <div className="flex gap-2">
                        <button
                            type="button"
                            onClick={() => setProposalData({
                                total_capex: 150000.00,
                                monthly_payment: 15000.00,
                                total_materials: 120000.00,
                                total_labor: 20000.00,
                                total_services: 10000.00,
                                summary: { margin_percent: 0.15 },
                                materials_table: [
                                    { item: "Switch Core Mock", qty: 2, total_price: 20000.00 },
                                    { item: "AP Wi-Fi 6 Mock", qty: 10, total_price: 15000.00 }
                                ],
                                labor_table: [
                                    { role: "Analista Sênior", hours: 40, total_price: 10000.00 }
                                ],
                                services_table: [
                                    { service_name: "Instalação Física", total_price: 5000.00 }
                                ]
                            })}
                            className="text-xs text-gray-400 hover:text-gray-600 underline mr-2"
                        >
                            Forçar Mock (Dev)
                        </button>
                        <Button variant="outline" size="sm" onClick={handleCalculate} isLoading={loading}>
                            <span className="material-symbols-outlined mr-2">refresh</span>
                            Recalcular
                        </Button>
                    </div>
                </div>

                {proposalData && (
                    <div className="space-y-6">
                        {/* Summary Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
                                <p className="text-xs text-blue-600 font-bold uppercase">CAPEX Total</p>
                                <p className="text-2xl font-bold text-blue-900">{formatCurrency(proposalData.total_capex)}</p>
                            </div>
                            <div className="p-4 bg-green-50 rounded-lg border border-green-100">
                                <p className="text-xs text-green-600 font-bold uppercase">Mensalidade (12x)</p>
                                <p className="text-2xl font-bold text-green-900">{formatCurrency(proposalData.monthly_payment)}</p>
                            </div>
                            <div className="p-4 bg-amber-50 rounded-lg border border-amber-100">
                                <p className="text-xs text-amber-600 font-bold uppercase">Margem Global</p>
                                <p className="text-2xl font-bold text-amber-900">{((proposalData.summary?.margin_percent || 0) * 100).toFixed(1)}%</p>
                            </div>
                        </div>

                        {/* Cost Breakdown */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                            {/* Materials */}
                            <div className="border rounded-lg overflow-hidden">
                                <div className="bg-gray-50 px-4 py-2 border-b flex justify-between items-center">
                                    <h4 className="font-bold text-sm text-gray-700">Materiais & Hardware</h4>
                                    <span className="text-xs font-mono bg-white px-2 py-1 rounded border">{formatCurrency(proposalData.total_materials)}</span>
                                </div>
                                <div className="p-0 max-h-48 overflow-y-auto">
                                    <table className="w-full text-xs">
                                        <thead className="bg-gray-50 sticky top-0">
                                            <tr>
                                                <th className="px-3 py-1 text-left">Item</th>
                                                <th className="px-3 py-1 text-right">Qtd</th>
                                                <th className="px-3 py-1 text-right">Total</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {proposalData.materials_table?.map((m, i) => (
                                                <tr key={i} className="border-b last:border-0 hover:bg-gray-50">
                                                    <td className="px-3 py-2 truncate max-w-[200px]" title={m.item}>{m.item}</td>
                                                    <td className="px-3 py-2 text-right">{m.qty}</td>
                                                    <td className="px-3 py-2 text-right font-medium">{formatCurrency(m.total_price)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            {/* Labor & Services */}
                            <div className="border rounded-lg overflow-hidden">
                                <div className="bg-gray-50 px-4 py-2 border-b flex justify-between items-center">
                                    <h4 className="font-bold text-sm text-gray-700">Serviços & Mão de Obra</h4>
                                    <span className="text-xs font-mono bg-white px-2 py-1 rounded border">{formatCurrency(proposalData.total_labor + proposalData.total_services)}</span>
                                </div>
                                <div className="p-0 max-h-48 overflow-y-auto">
                                    <table className="w-full text-xs">
                                        <thead className="bg-gray-50 sticky top-0">
                                            <tr>
                                                <th className="px-3 py-1 text-left">Atividade</th>
                                                <th className="px-3 py-1 text-right">Hrs</th>
                                                <th className="px-3 py-1 text-right">Total</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {[...(proposalData.labor_table || []), ...(proposalData.services_table || [])].map((s, i) => (
                                                <tr key={i} className="border-b last:border-0 hover:bg-gray-50">
                                                    <td className="px-3 py-2 truncate max-w-[200px]" title={s.service_name || s.role}>{s.service_name || s.role}</td>
                                                    <td className="px-3 py-2 text-right">{s.hours || '-'}</td>
                                                    <td className="px-3 py-2 text-right font-medium">{formatCurrency(s.total_price)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                        </div>
                    </div>
                )}
            </div>

            <div className="flex justify-between pt-4">
                <Button variant="outline" size="lg" onClick={onBack}>
                    Voltar
                </Button>
                <Button size="lg" onClick={() => onNext(proposalData)} className="shadow-lg shadow-blue-500/20" disabled={!proposalData}>
                    Confirmar Valores
                    <span className="material-symbols-outlined ml-2">arrow_forward</span>
                </Button>
            </div>
        </div>
    );
};
