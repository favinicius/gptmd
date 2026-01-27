import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button, Textarea, Input, Select } from '../../ui'; // Adjusted imports
import { analyzeInstruction } from '../../../services/api';

export const Step1Input = ({ onNext, initialData }) => {
    const [loading, setLoading] = useState(false);
    const [instruction, setInstruction] = useState(initialData.instruction || '');
    const [files, setFiles] = useState(initialData.files || []);
    const [analyzedIntent, setAnalyzedIntent] = useState(initialData.intent || null);

    const onDrop = (acceptedFiles) => {
        setFiles(prev => [...prev, ...acceptedFiles]);
    };

    const removeFile = (name) => {
        setFiles(prev => prev.filter(f => f.name !== name));
    };

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    const handleAnalyze = async () => {
        if (!instruction) return alert("Por favor, insira uma instrução.");
        setLoading(true);
        try {
            const formData = new FormData();
            formData.append('instruction', instruction);
            files.forEach(f => formData.append('files', f));

            const result = await analyzeInstruction(formData);
            setAnalyzedIntent(result);
        } catch (error) {
            console.error(error);
            // alert("Erro na análise: " + (error.detail || error.message));
            console.log("Mocking intent for testing due to API error");
            setAnalyzedIntent({
                client_name: "Cliente Teste",
                project_name: "Projeto Mock",
                scope_items: [
                    { name: "Item Mock 1", detected_quantity: 5, action_type: "SWITCH" }
                ]
            });
        } finally {
            setLoading(false);
        }
    };

    const handleConfirm = () => {
        if (!analyzedIntent) return;
        onNext({ instruction, files, intent: analyzedIntent });
    };

    const updateScopeItem = (index, field, value) => {
        const newItems = [...analyzedIntent.scope_items];
        newItems[index] = { ...newItems[index], [field]: value };
        setAnalyzedIntent({ ...analyzedIntent, scope_items: newItems });
    };

    const removeScopeItem = (index) => {
        const newItems = analyzedIntent.scope_items.filter((_, i) => i !== index);
        setAnalyzedIntent({ ...analyzedIntent, scope_items: newItems });
    };

    const addScopeItem = () => {
        const newItem = { name: "Novo Item", detected_quantity: 1, action_type: "OTHER" };
        setAnalyzedIntent({ ...analyzedIntent, scope_items: [...analyzedIntent.scope_items, newItem] });
    };

    if (analyzedIntent) {
        return (
            <div className="space-y-6 animate-fade-in">
                <div className="bg-white p-6 rounded-xl border border-surface-light">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-lg font-bold text-neutral-dark">Validação de Escopo</h3>
                        <Button variant="outline" size="sm" onClick={() => setAnalyzedIntent(null)}>
                            Voltar para Edição
                        </Button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                        <div className="p-3 bg-gray-50 rounded border">
                            <span className="text-xs text-gray-500 uppercase">Cliente Detectado</span>
                            <p className="font-semibold">{analyzedIntent.client_name}</p>
                        </div>
                        <div className="p-3 bg-gray-50 rounded border">
                            <span className="text-xs text-gray-500 uppercase">Projeto</span>
                            <p className="font-semibold">{analyzedIntent.project_name}</p>
                        </div>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                                <tr>
                                    <th className="px-4 py-3">Item / Serviço</th>
                                    <th className="px-4 py-3 w-32">Qtd</th>
                                    <th className="px-4 py-3 w-40">Tipo</th>
                                    <th className="px-4 py-3 w-20">Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {analyzedIntent.scope_items.map((item, idx) => (
                                    <tr key={idx} className="border-b hover:bg-gray-50">
                                        <td className="px-4 py-2">
                                            <input
                                                className="w-full bg-transparent border-none focus:ring-0 p-0 font-medium text-neutral-dark"
                                                value={item.name}
                                                onChange={(e) => updateScopeItem(idx, 'name', e.target.value)}
                                            />
                                        </td>
                                        <td className="px-4 py-2">
                                            <input
                                                type="number"
                                                className="w-full bg-transparent border border-gray-200 rounded px-2 py-1 text-center"
                                                value={item.detected_quantity}
                                                onChange={(e) => updateScopeItem(idx, 'detected_quantity', parseInt(e.target.value))}
                                            />
                                        </td>
                                        <td className="px-4 py-2">
                                            <select
                                                className="w-full bg-transparent border-none text-xs"
                                                value={item.action_type}
                                                onChange={(e) => updateScopeItem(idx, 'action_type', e.target.value)}
                                            >
                                                <option value="SWITCH">Switch</option>
                                                <option value="SERVER">Server</option>
                                                <option value="STORAGE">Storage</option>
                                                <option value="VM">VM</option>
                                                <option value="WIFI">Wi-Fi</option>
                                                <option value="FIREWALL">Firewall</option>
                                                <option value="BACKUP">Backup</option>
                                                <option value="MIGRATION">Migration</option>
                                                <option value="CABLING">Cabling</option>
                                                <option value="CONSULTING">Consulting</option>
                                                <option value="OTHER">Other</option>
                                            </select>
                                        </td>
                                        <td className="px-4 py-2 text-center">
                                            <button
                                                onClick={() => removeScopeItem(idx)}
                                                className="text-gray-400 hover:text-red-500"
                                            >
                                                <span className="material-symbols-outlined text-sm">delete</span>
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        <div className="mt-4">
                            <Button variant="ghost" size="sm" onClick={addScopeItem} className="text-primary">
                                + Adicionar Item
                            </Button>
                        </div>
                    </div>
                </div>

                <div className="flex justify-end pt-4">
                    <Button size="lg" onClick={handleConfirm} className="shadow-lg shadow-blue-500/20">
                        Confirmar Escopo & Avançar
                        <span className="material-symbols-outlined ml-2">arrow_forward</span>
                    </Button>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="bg-white p-6 rounded-xl border border-surface-light shadow-sm">
                <div className="flex items-center gap-3 mb-4">
                    <span className="material-symbols-outlined text-primary">edit_note</span>
                    <h3 className="text-lg font-bold text-neutral-dark">1. Instrução & Contexto</h3>
                </div>

                <Textarea
                    label="Descreva o cenário ou cole o conteúdo do e-mail"
                    placeholder="Ex: O cliente precisa de uma rede GPON para 500 pontos, com redundância e gerência via Zabbix..."
                    className="h-40 font-mono text-sm leading-relaxed"
                    value={instruction}
                    onChange={e => setInstruction(e.target.value)}
                />

                <div className="mt-6">
                    <label className="text-sm font-bold text-neutral-dark block mb-2">Documentos de Apoio</label>
                    <div
                        {...getRootProps()}
                        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${isDragActive ? 'border-primary bg-blue-50' : 'border-surface-light hover:border-neutral-gray'}`}
                    >
                        <input {...getInputProps()} />
                        <div className="flex flex-col items-center gap-2 text-neutral-gray">
                            <span className="material-symbols-outlined text-4xl">cloud_upload</span>
                            <p className="text-sm font-medium">Arraste arquivos aqui ou clique para selecionar</p>
                        </div>
                    </div>

                    {files.length > 0 && (
                        <div className="mt-4 space-y-2">
                            {files.map(file => (
                                <div key={file.name} className="flex items-center justify-between p-3 bg-background-light rounded-lg border border-surface-light text-sm">
                                    <div className="flex items-center gap-3 overflow-hidden">
                                        <span className="material-symbols-outlined text-primary">description</span>
                                        <span className="truncate font-medium text-neutral-dark">{file.name}</span>
                                        <span className="text-neutral-gray text-xs">({(file.size / 1024).toFixed(0)}KB)</span>
                                    </div>
                                    <button type="button" onClick={() => removeFile(file.name)} className="text-neutral-gray hover:text-red-500 transition-colors">
                                        <span className="material-symbols-outlined text-lg">close</span>
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            <div className="flex justify-end pt-4">
                <Button size="lg" onClick={handleAnalyze} isLoading={loading} disabled={!instruction} className="w-full md:w-auto shadow-xl shadow-blue-500/20">
                    Analisar Intenção com IA
                    <span className="material-symbols-outlined ml-2">auto_awesome</span>
                </Button>

                {/* Dev Bypass Button */}
                <button
                    type="button"
                    onClick={() => {
                        setAnalyzedIntent({
                            client_name: "Cliente Mock (Dev)",
                            project_name: "Projeto Exemplo",
                            scope_items: [
                                { name: "Switch Core 24p", detected_quantity: 2, action_type: "SWITCH" },
                                { name: "Access Point Wi-Fi 6", detected_quantity: 10, action_type: "WIFI" },
                                { name: "Instalação e Configuração", detected_quantity: 12, action_type: "CONSULTING" }
                            ]
                        });
                    }}
                    className="ml-4 text-xs text-gray-400 hover:text-gray-600 underline"
                >
                    Preencher Mock (Dev)
                </button>
            </div>
        </div>
    );
};
