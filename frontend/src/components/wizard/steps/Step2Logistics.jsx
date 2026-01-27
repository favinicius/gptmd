import React, { useState, useEffect } from 'react';
import { Button, Input, Select, Textarea } from '../../ui';
import { planLogistics } from '../../../services/api';

export const LogisticsForm = ({ onNext, onBack, initialData, intent }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState(initialData || {
        requires_flight: false,
        flight_region: null,
        requires_car_rental: false,
        estimated_daily_km: 0,
        requires_freight: false,
        hotel_tier: 'hotel_tier_interior',
        origin_mobilization_km: 0,
        team_size: 1,
        duration_days: 5,
        stay_duration_days: []
    });

    const handleAutoPlan = async () => {
        setLoading(true);
        try {
            const plan = await planLogistics(intent);
            setFormData(prev => ({
                ...prev,
                ...plan,
                team_size: intent.logistics_override?.team_size || 1 // Keep manually set team size if any
            }));
        } catch (error) {
            console.error(error);
            alert("Erro no planejamento automático: " + error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = () => {
        // Validation logic can go here
        onNext(formData);
    };

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="bg-white p-6 rounded-xl border border-surface-light shadow-sm">
                <div className="flex justify-between items-center mb-6">
                    <div className="flex items-center gap-3">
                        <span className="material-symbols-outlined text-primary">flight_takeoff</span>
                        <h3 className="text-lg font-bold text-neutral-dark">2. Planejamento Logístico</h3>
                    </div>
                    <Button variant="outline" size="sm" onClick={handleAutoPlan} isLoading={loading}>
                        <span className="material-symbols-outlined mr-2">auto_awesome</span>
                        Sugerir com IA
                    </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                        <h4 className="text-sm font-bold text-gray-700 uppercase border-b pb-2">Transporte & Deslocamento</h4>

                        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <label className="text-sm font-medium">Requer Aéreo?</label>
                            <input
                                type="checkbox"
                                className="w-5 h-5 text-primary rounded"
                                checked={formData.requires_flight}
                                onChange={e => setFormData({ ...formData, requires_flight: e.target.checked })}
                            />
                        </div>

                        {formData.requires_flight && (
                            <Select
                                label="Região do Voo"
                                value={formData.flight_region || ''}
                                onChange={e => setFormData({ ...formData, flight_region: e.target.value })}
                                options={[
                                    { value: 'flight_s_se', label: 'Sul / Sudeste' },
                                    { value: 'flight_ne', label: 'Norte / Nordeste / CO' }
                                ]}
                            />
                        )}

                        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <label className="text-sm font-medium">Aluguel de Carro (SUV/Pick-up)</label>
                            <input
                                type="checkbox"
                                className="w-5 h-5 text-primary rounded"
                                checked={formData.requires_car_rental}
                                onChange={e => setFormData({ ...formData, requires_car_rental: e.target.checked })}
                            />
                        </div>

                        {formData.requires_car_rental && (
                            <Input
                                label="KM Diário Estimado"
                                type="number"
                                value={formData.estimated_daily_km}
                                onChange={e => setFormData({ ...formData, estimated_daily_km: parseFloat(e.target.value) })}
                            />
                        )}

                        <Input
                            label="Deslocamento Inicial (KM - Ida/Volta)"
                            type="number"
                            value={formData.origin_mobilization_km}
                            onChange={e => setFormData({ ...formData, origin_mobilization_km: parseFloat(e.target.value) })}
                            helpText="Distância rodoviária até o local (se não for aéreo)"
                        />

                    </div>

                    <div className="space-y-4">
                        <h4 className="text-sm font-bold text-gray-700 uppercase border-b pb-2">Hospedagem & Equipe</h4>

                        <Select
                            label="Padrão de Hotel"
                            value={formData.hotel_tier}
                            onChange={e => setFormData({ ...formData, hotel_tier: e.target.value })}
                            options={[
                                { value: 'hotel_tier_interior', label: 'Interior / Padrão' },
                                { value: 'hotel_tier_capital', label: 'Capital / Executivo' }
                            ]}
                        />

                        <div className="grid grid-cols-2 gap-4">
                            <Input
                                label="Tamanho da Equipe"
                                type="number"
                                value={formData.team_size}
                                onChange={e => setFormData({ ...formData, team_size: parseInt(e.target.value) })}
                            />
                            <Input
                                label="Duração Total (Dias)"
                                type="number"
                                value={formData.duration_days}
                                onChange={e => setFormData({ ...formData, duration_days: parseInt(e.target.value) })}
                            />
                        </div>
                    </div>
                </div>
            </div>

            <div className="flex justify-between pt-4">
                <Button variant="outline" size="lg" onClick={onBack}>
                    Voltar
                </Button>
                <Button size="lg" onClick={handleSubmit} className="shadow-lg shadow-blue-500/20">
                    Confirmar Logística
                    <span className="material-symbols-outlined ml-2">arrow_forward</span>
                </Button>
            </div>
        </div>
    );
};
