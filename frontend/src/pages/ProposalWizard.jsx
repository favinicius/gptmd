import React, { useState } from 'react';
import { Stepper } from '../components/wizard/Stepper';
import { Step1Input } from '../components/wizard/steps/Step1Input';
import { LogisticsForm } from '../components/wizard/steps/Step2Logistics';
import { PricingDashboard } from '../components/wizard/steps/Step3Pricing';
import { RedactionEditor } from '../components/wizard/steps/Step4Redaction';
import { ConclusionStep } from '../components/wizard/steps/Step5Conclusion';

const ProposalWizard = () => {
    const [currentStep, setCurrentStep] = useState(1);
    const [wizardData, setWizardData] = useState({
        instruction: '',
        files: [],
        intent: null,
        logisticsPlan: null,
        proposal: null,
        textBlocks: {}
    });

    const steps = [
        { id: 1, label: 'Instrução & Escopo', icon: 'description' },
        { id: 2, label: 'Logística', icon: 'flight_takeoff' },
        { id: 3, label: 'Financeiro', icon: 'attach_money' },
        { id: 4, label: 'Redação Técnica', icon: 'edit_note' },
        { id: 5, label: 'Conclusão', icon: 'check_circle' }
    ];

    const nextStep = () => setCurrentStep(prev => Math.min(prev + 1, steps.length));
    const prevStep = () => setCurrentStep(prev => Math.max(prev - 1, 1));

    const updateWizardData = (key, value) => {
        setWizardData(prev => ({ ...prev, [key]: value }));
    };

    return (
        <div className="space-y-8">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-neutral-dark">Nova Proposta Técnica</h1>
                <p className="text-neutral-gray">Utilize o assistente abaixo para gerar uma proposta validada.</p>
            </header>

            {/* Stepper Component */}
            <Stepper steps={steps} currentStep={currentStep} />

            {/* Step Content */}
            <div className="mt-8">
                {currentStep === 1 && (
                    <Step1Input
                        onNext={(data) => {
                            updateWizardData('instruction', data.instruction);
                            updateWizardData('files', data.files);
                            updateWizardData('intent', data.intent);
                            nextStep();
                        }}
                        initialData={{
                            instruction: wizardData.instruction,
                            files: wizardData.files,
                            intent: wizardData.intent
                        }}
                    />
                )}
                {currentStep === 2 && (
                    <LogisticsForm
                        onNext={(data) => {
                            updateWizardData('logisticsPlan', data);
                            nextStep();
                        }}
                        onBack={prevStep}
                        initialData={wizardData.logisticsPlan}
                        intent={wizardData.intent}
                    />
                )}
                {currentStep === 3 && (
                    <PricingDashboard
                        onNext={(data) => {
                            updateWizardData('proposal', data);
                            nextStep();
                        }}
                        onBack={prevStep}
                        initialData={wizardData.proposal}
                        intent={wizardData.intent}
                        logisticsPlan={wizardData.logisticsPlan}
                    />
                )}
                {currentStep === 4 && (
                    <RedactionEditor
                        onNext={(data) => {
                            updateWizardData('textBlocks', data);
                            nextStep();
                        }}
                        onBack={prevStep}
                        initialData={wizardData.textBlocks}
                        intent={wizardData.intent}
                        proposal={wizardData.proposal}
                    />
                )}
                {currentStep === 5 && (
                    <ConclusionStep
                        onReset={() => {
                            setCurrentStep(1);
                            setWizardData({
                                instruction: '',
                                files: [],
                                intent: null,
                                logisticsPlan: null,
                                proposal: null,
                                textBlocks: {}
                            });
                        }}
                        intent={wizardData.intent}
                        proposal={wizardData.proposal}
                        textBlocks={wizardData.textBlocks}
                    />
                )}
            </div>
        </div>
    );
};

export default ProposalWizard;
