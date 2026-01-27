import React, { useState, useEffect } from 'react';
import { Button, Textarea } from '../../ui';
import { generateRedaction } from '../../../services/api';

export const RedactionEditor = ({ onNext, onBack, initialData, intent, proposal }) => {
    const [loading, setLoading] = useState(false);
    const [textBlocks, setTextBlocks] = useState(initialData || {});
    // State to toggle between "Loading" and "Content" for Dev UX if waiting
    const [hasLoaded, setHasLoaded] = useState(!!initialData);

    useEffect(() => {
        if (!initialData && intent && proposal && !hasLoaded) {
            handleGenerate();
        }
    }, []);

    const handleGenerate = async () => {
        setLoading(true);
        try {
            const result = await generateRedaction(intent, proposal);
            setTextBlocks(result);
            setHasLoaded(true);
        } catch (error) {
            console.error(error);
            // Don't alert here to avoid spamming if it hangs. The user can use the mock button.
        } finally {
            setLoading(false);
        }
    };

    const handleMock = () => {
        setTextBlocks({
            introduction: "Esta proposta técnica visa modernizar a infraestrutura de rede da empresa...",
            solution_description: "A solução proposta inclui a implementação de Switches de alta performance e cobertura Wi-Fi 6...",
            methodology: "O projeto seguirá as fases de Site Survey, Instalação Física, Configuração Lógica e Testes de Aceitação...",
            logistics: "A equipe técnica será mobilizada via transporte aéreo e contará com hospedagem local..."
        });
        setHasLoaded(true);
        setLoading(false);
    };

    if (loading && !hasLoaded) {
        return (
            <div className="flex flex-col items-center justify-center p-12 space-y-4 animate-fade-in relative">
                <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
                <p className="text-neutral-gray font-medium">Escrevendo redação técnica com IA...</p>
                <button
                    onClick={handleMock}
                    className="absolute bottom-4 text-xs text-gray-400 underline hover:text-gray-600"
                >
                    Demorando muito? Usar Mock (Dev)
                </button>
            </div>
        );
    }

    const sections = [
        { key: 'introduction', label: '1. Introdução & Contexto' },
        { key: 'solution_description', label: '2. Descrição da Solução' },
        { key: 'methodology', label: '3. Metodologia de Execução' },
        { key: 'logistics', label: '4. Detalhes Logísticos' }
    ];

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="bg-white p-6 rounded-xl border border-surface-light shadow-sm">
                <div className="flex justify-between items-center mb-6">
                    <div className="flex items-center gap-3">
                        <span className="material-symbols-outlined text-primary">edit_note</span>
                        <h3 className="text-lg font-bold text-neutral-dark">4. Redação Técnica</h3>
                    </div>
                    <div className="flex gap-2">
                        <button onClick={handleMock} className="text-xs text-gray-400 hover:text-gray-600 underline mr-2">
                            Forçar Mock
                        </button>
                        <Button variant="outline" size="sm" onClick={handleGenerate} isLoading={loading}>
                            <span className="material-symbols-outlined mr-2">refresh</span>
                            Reescrever
                        </Button>
                    </div>
                </div>

                <div className="space-y-6">
                    {sections.map(({ key, label }) => (
                        <div key={key}>
                            <label className="block text-sm font-bold text-neutral-dark mb-2">{label}</label>
                            <Textarea
                                value={textBlocks[key] || ''}
                                onChange={(e) => setTextBlocks({ ...textBlocks, [key]: e.target.value })}
                                className="min-h-[120px] text-sm"
                            />
                        </div>
                    ))}
                </div>
            </div>

            <div className="flex justify-between pt-4">
                <Button variant="outline" size="lg" onClick={onBack}>
                    Voltar
                </Button>
                <Button size="lg" onClick={() => onNext(textBlocks)} className="shadow-lg shadow-blue-500/20">
                    Finalizar Redação
                    <span className="material-symbols-outlined ml-2">arrow_forward</span>
                </Button>
            </div>
        </div>
    );
};
