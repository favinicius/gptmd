import React from 'react';
import { cn } from '../Layout';

// DS Button
export const Button = ({ children, variant = 'primary', size = 'default', className, isLoading, disabled, ...props }) => {
    const variants = {
        primary: "bg-primary text-white hover:bg-blue-700 shadow-sm",
        secondary: "bg-white text-neutral-dark border border-surface-light hover:bg-gray-50",
        ghost: "bg-transparent text-neutral-gray hover:bg-gray-100",
        danger: "bg-red-500 text-white hover:bg-red-600"
    };

    const sizes = {
        sm: "px-3 py-1.5 text-xs font-bold",
        default: "h-10 px-4 text-sm font-bold",
        lg: "h-12 px-6 text-base font-bold"
    };

    return (
        <button
            className={cn(
                "inline-flex items-center justify-center transition-colors rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 disabled:opacity-50 disabled:cursor-not-allowed",
                variants[variant],
                sizes[size],
                className
            )}
            disabled={disabled || isLoading}
            {...props}
        >
            {isLoading && <span className="material-symbols-outlined animate-spin mr-2 text-sm">progress_activity</span>}
            {children}
        </button>
    );
};

// DS Input
export const Input = ({ label, error, className, ...props }) => (
    <div className="space-y-1">
        {label && <label className="text-sm font-bold text-neutral-dark block">{label}</label>}
        <input
            className={cn(
                "w-full h-12 px-4 rounded-lg bg-background-light border border-surface-light text-neutral-dark text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all placeholder:text-neutral-gray",
                error && "bg-red-50 border-red-500 focus:ring-red-500 focus:border-red-500 text-red-900",
                className
            )}
            {...props}
        />
        {error && (
            <div className="flex items-center gap-1 text-red-600 mt-1">
                <span className="material-symbols-outlined !text-sm">error</span>
                <span className="text-xs font-medium">{error}</span>
            </div>
        )}
    </div>
);

// DS Select
export const Select = ({ label, options, error, className, ...props }) => (
    <div className="space-y-1">
        {label && <label className="text-sm font-bold text-neutral-dark block">{label}</label>}
        <div className="relative">
            <select
                className={cn(
                    "w-full h-12 px-4 rounded-lg bg-background-light border border-surface-light text-neutral-dark text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all appearance-none",
                    error && "bg-red-50 border-red-500 focus:ring-red-500",
                    className
                )}
                {...props}
            >
                {options.map(opt => (
                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
            </select>
            {/* Custom arrow could go here */}
            <span className="material-symbols-outlined absolute right-3 top-3 text-neutral-gray pointer-events-none">expand_more</span>
        </div>
        {error && <span className="text-xs text-red-500 font-medium">{error}</span>}
    </div>
);

// DS Textarea
export const Textarea = ({ label, error, className, ...props }) => (
    <div className="space-y-1">
        {label && <label className="text-sm font-bold text-neutral-dark block">{label}</label>}
        <textarea
            className={cn(
                "w-full px-4 py-3 border border-surface-light bg-background-light rounded-lg text-sm text-neutral-dark focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all min-h-[120px] placeholder:text-neutral-gray",
                error && "border-red-500 focus:ring-red-500 bg-red-50",
                className
            )}
            {...props}
        />
        {error && <span className="text-xs text-red-500 font-medium">{error}</span>}
    </div>
);
