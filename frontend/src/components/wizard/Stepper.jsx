import React from 'react';

export const Stepper = ({ steps, currentStep }) => {
    return (
        <div className="w-full py-4">
            <div className="flex items-center justify-between relative">
                {/* Connecting Line (Proportional Width) */}
                <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-1 bg-surface-light -z-10 rounded-full"></div>

                {/* Active Line Progress */}
                <div
                    className="absolute left-0 top-1/2 transform -translate-y-1/2 h-1 bg-primary -z-10 rounded-full transition-all duration-500 ease-in-out"
                    style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
                ></div>

                {steps.map((step) => {
                    const isCompleted = currentStep > step.id;
                    const isActive = currentStep === step.id;

                    return (
                        <div key={step.id} className="flex flex-col items-center gap-2 bg-background-light px-2 relative z-0">
                            <div
                                className={`
                                    w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-300
                                    ${isActive ? 'border-primary bg-primary text-white scale-110 shadow-lg shadow-blue-500/30' :
                                        isCompleted ? 'border-primary bg-primary text-white' :
                                            'border-neutral-gray bg-white text-neutral-gray'}
                                `}
                            >
                                {isCompleted ? (
                                    <span className="material-symbols-outlined text-sm font-bold">check</span>
                                ) : (
                                    <span className="material-symbols-outlined text-sm">{step.icon}</span>
                                )}
                            </div>
                            <span className={`text-xs font-semibold whitespace-nowrap hidden md:block transition-colors ${isActive ? 'text-primary' : isCompleted ? 'text-neutral-dark' : 'text-neutral-gray'}`}>
                                {step.label}
                            </span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
