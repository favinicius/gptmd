import React, { useState } from 'react';
import ProposalForm from '../components/forms/ProposalForm';
import MarkdownViewer from '../components/MarkdownViewer';
import axios from 'axios';

const NewProposal = () => {
    const [result, setResult] = useState(null);
    const [selectedTab, setSelectedTab] = useState(0);
    const [fileContent, setFileContent] = useState("");
    const [loadingContent, setLoadingContent] = useState(false);

    const handleSuccess = (data) => {
        console.log("Success Data:", data);
        setResult(data);
        if (data.files && data.files.length > 0) {
            fetchFileContent(data.files[0]);
        }
    };

    const fetchFileContent = async (filePath) => {
        setLoadingContent(true);
        try {
            // filePath vem absoluto do backend ex: /Users/.../output/2026.../PROPOSTA.md
            // Preciso converter para URL relativa do static mount /output
            // O backend retorna output_dir absoluto.
            // Vou assumir que o backend pode ser ajustado para retornar relativo, ou faço um truque aqui.
            // Truque: Pegar tudo depois de "output/" na string.

            const parts = filePath.split("output/");
            if (parts.length < 2) return;
            const relativePath = parts[1];

            const url = `http://localhost:8000/output/${relativePath}`;
            const res = await axios.get(url);
            setFileContent(res.data);
        } catch (error) {
            console.error("Erro ao baixar arquivo", error);
            setFileContent("**Erro ao carregar preview do arquivo.**");
        } finally {
            setLoadingContent(false);
        }
    };

    return (
        <div className="max-w-5xl mx-auto space-y-8">
            <header>
                <h1 className="text-3xl font-bold text-slate-900">Nova Proposta</h1>
                <p className="text-slate-500">Preencha os dados abaixo para gerar a proposta técnica.</p>
            </header>

            {!result ? (
                <ProposalForm onSuccess={handleSuccess} />
            ) : (
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                    <div className="p-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
                        <h2 className="font-semibold text-slate-700">Resultado da Geração</h2>
                        <button
                            onClick={() => setResult(null)}
                            className="text-sm text-blue-600 hover:underline"
                        >
                            Criar Nova
                        </button>
                    </div>

                    {/* Tabs for Files */}
                    <div className="flex border-b border-slate-200 overflow-x-auto">
                        {result.files.map((file, idx) => {
                            const fileName = file.split('/').pop().split('\\').pop(); // Handle both separators
                            return (
                                <button
                                    key={idx}
                                    onClick={() => { setSelectedTab(idx); fetchFileContent(file); }}
                                    className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${selectedTab === idx
                                            ? "border-blue-500 text-blue-600 bg-white"
                                            : "border-transparent text-slate-500 hover:text-slate-700 hover:bg-slate-50"
                                        }`}
                                >
                                    {fileName}
                                </button>
                            );
                        })}
                    </div>

                    {/* Content Preview */}
                    <div className="p-8 bg-white min-h-[500px]">
                        {loadingContent ? (
                            <div className="flex items-center justify-center h-40">
                                <span className="text-slate-400 animate-pulse">Carregando preview...</span>
                            </div>
                        ) : (
                            <MarkdownViewer content={fileContent} />
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default NewProposal;
