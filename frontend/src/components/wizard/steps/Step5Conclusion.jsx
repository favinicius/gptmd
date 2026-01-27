import React, { useState } from 'react';
import { Button } from '../../ui';
import { assembleProposal } from '../../../services/api';

export const ConclusionStep = ({ onReset, intent, proposal, textBlocks }) => {
    const [loading, setLoading] = useState(false);
    const [generatedFiles, setGeneratedFiles] = useState(null);

    const handleAssemble = async () => {
        setLoading(true);
        try {
            const result = await assembleProposal(intent, proposal, textBlocks);
            setGeneratedFiles(result.files);
        } catch (error) {
            console.error(error);
            // alert("Erro na montagem: " + error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleMockAssemble = () => {
        setLoading(true);
        setTimeout(() => {
            setGeneratedFiles([
                "/downloads/proposta_tecnica_v1.md",
                "/downloads/proposta_comercial_v1.csv"
            ]);
            setLoading(false);
        }, 1500);
    };

    if (generatedFiles) {
        return (
            <div className="flex flex-col items-center justify-center p-12 space-y-6 animate-fade-in bg-white rounded-xl border border-surface-light shadow-sm">
                <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-4">
                    <span className="material-symbols-outlined text-4xl">check_circle</span>
                </div>
                <h3 className="text-2xl font-bold text-neutral-dark">Proposta Gerada com Sucesso!</h3>
                <p className="text-gray-600 text-center max-w-md">
                    Os arquivos foram compilados e estão prontos para download.
                </p>

                <div className="w-full max-w-md bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <h4 className="text-sm font-bold text-gray-700 uppercase mb-3">Arquivos Gerados:</h4>
                    <ul className="space-y-2">
                        {generatedFiles.map((file, idx) => (
                            <li key={idx} className="flex items-center gap-2 p-2 bg-white rounded border border-gray-200 text-sm hover:text-primary transition-colors cursor-pointer">
                                <span className="material-symbols-outlined text-gray-400">description</span>
                                <span className="truncate">{file.split('/').pop()}</span>
                                <span className="material-symbols-outlined text-gray-400 ml-auto text-xs">download</span>
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="flex gap-4 pt-4">
                    <Button variant="outline" onClick={onReset}>
                        Criar Nova Proposta
                    </Button>
                    <Button onClick={() => alert("Funcionalidade de Download real seria via link direto.")}>
                        Baixar Todos (.zip)
                    </Button>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="bg-white p-6 rounded-xl border border-surface-light shadow-sm text-center py-12">

                <div className="mb-8">
                    <div className="w-20 h-20 bg-blue-50 text-primary rounded-full flex items-center justify-center mx-auto mb-4">
                        <span className="material-symbols-outlined text-5xl">inventory_2</span>
                    </div>
                    <h3 className="text-xl font-bold text-neutral-dark">Pronto para Finalizar</h3>
                    <p className="text-gray-600 max-w-lg mx-auto mt-2">
                        Você revisou o escopo, logística, preços e redação. Clique abaixo para compilar os documentos finais da proposta.
                    </p>
                </div>

                <div className="flex flex-col items-center gap-4">
                    <Button size="lg" onClick={handleAssemble} isLoading={loading} className="w-full md:w-64 shadow-xl shadow-blue-500/20">
                        Gerar Documentos Finais
                        <span className="material-symbols-outlined ml-2">rocket_launch</span>
                    </Button>

                    <button
                        onClick={handleMockAssemble}
                        className="text-sm text-gray-400 hover:text-gray-600 underline"
                    >
                        Simular Geração (Dev Mock)
                    </button>

                    <button
                        onClick={onReset}
                        className="text-sm text-red-400 hover:text-red-600 font-medium mt-4"
                    >
                        Cancelar e Reiniciar
                    </button>
                </div>
            </div>
        </div>
    );
};
