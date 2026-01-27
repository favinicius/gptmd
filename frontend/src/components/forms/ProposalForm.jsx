import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button, Input, Select, Textarea } from '../ui';
import { generateProposal } from '../../services/api';

const ProposalForm = ({ onSuccess }) => {
    const [loading, setLoading] = useState(false);
    const [files, setFiles] = useState([]);
    const [formData, setFormData] = useState({
        instruction: '',
        sizing: 'standard',
        contingency: 'standard',
        term: 30,
        output_mode: 'unified',
        separate_opex: false
    });

    const onDrop = (acceptedFiles) => {
        setFiles(prev => [...prev, ...acceptedFiles]);
    };

    const removeFile = (name) => {
        setFiles(prev => prev.filter(f => f.name !== name));
    };

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!formData.instruction) return alert("Instrução é obrigatória");

        setLoading(true);
        try {
            const payload = new FormData();
            payload.append('instruction', formData.instruction);
            payload.append('sizing', formData.sizing);
            payload.append('contingency', formData.contingency);
            payload.append('term', formData.term);
            payload.append('output_mode', formData.output_mode);
            payload.append('separate_opex', formData.separate_opex);

            files.forEach(file => {
                payload.append('files', file);
            });

            const result = await generateProposal(payload);
            if (onSuccess) onSuccess(result);

        } catch (error) {
            alert("Erro na geração: " + (error.detail || error.message));
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-8">
            {/* 1. Prompt Section */}
            <section className="bg-white p-6 rounded-xl border border-surface-light shadow-sm">
                <div className="flex items-center gap-3 mb-4">
                    <span className="material-symbols-outlined text-primary">edit_note</span>
                    <h3 className="text-lg font-bold text-neutral-dark">1. Instrução & Contexto</h3>
                </div>

                <Textarea
                    label="Descreva o cenário ou cole o conteúdo do e-mail"
                    placeholder="Ex: O cliente precisa de uma rede GPON para 500 pontos, com redundância e gerência via Zabbix..."
                    className="h-40 font-mono text-sm leading-relaxed"
                    value={formData.instruction}
                    onChange={e => setFormData({ ...formData, instruction: e.target.value })}
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
            </section>

            {/* 2. Parameters Section */}
            <section className="bg-white p-6 rounded-xl border border-surface-light shadow-sm">
                <div className="flex items-center gap-3 mb-4">
                    <span className="material-symbols-outlined text-primary">tune</span>
                    <h3 className="text-lg font-bold text-neutral-dark">2. Parâmetros de Cálculo</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <Select
                        label="Dimensionamento (Sizing)"
                        value={formData.sizing}
                        onChange={e => setFormData({ ...formData, sizing: e.target.value })}
                        options={[
                            { value: 'aggressive', label: 'Agressivo (0.85x)' },
                            { value: 'standard', label: 'Padrão (1.0x)' },
                            { value: 'secure', label: 'Seguro (1.4x)' },
                            { value: 'critical', label: 'Crítico (1.6x)' }
                        ]}
                    />
                    <Select
                        label="Contingência (SHE)"
                        value={formData.contingency}
                        onChange={e => setFormData({ ...formData, contingency: e.target.value })}
                        options={[
                            { value: 'none', label: 'Nenhuma (0h)' },
                            { value: 'low', label: 'Baixa (1h/dia)' },
                            { value: 'standard', label: 'Padrão (1.5h/dia)' },
                            { value: 'high', label: 'Alta (2h/dia + 10%)' }
                        ]}
                    />
                    <Input
                        label="Prazo Pagamento (Dias)"
                        type="number"
                        value={formData.term}
                        onChange={e => setFormData({ ...formData, term: parseInt(e.target.value) })}
                    />
                    <Select
                        label="Modo de Saída"
                        value={formData.output_mode}
                        onChange={e => setFormData({ ...formData, output_mode: e.target.value })}
                        options={[
                            { value: 'unified', label: 'Unificado (Tech+Comm)' },
                            { value: 'full', label: 'Completo (3 Arqs)' },
                            { value: 'splited', label: 'Separado' }
                        ]}
                    />
                </div>

                <div className="mt-6 flex items-center gap-2">
                    <input
                        type="checkbox"
                        id="opex"
                        className="rounded text-blue-600 focus:ring-blue-500"
                        checked={formData.separate_opex}
                        onChange={e => setFormData({ ...formData, separate_opex: e.target.checked })}
                    />
                    <label htmlFor="opex" className="text-sm font-medium text-slate-700 cursor-pointer">
                        Gerar proposta de OPEX/Sustentação separada
                    </label>
                </div>
            </section>

            {/* Action Bar */}
            <div className="flex justify-end pt-4">
                <Button size="lg" isLoading={loading} className="w-full md:w-auto shadow-xl shadow-blue-500/20">
                    Gerar Proposta
                </Button>
            </div>
        </form>
    );
};

export default ProposalForm;
