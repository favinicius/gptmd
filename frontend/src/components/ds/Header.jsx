import React from 'react';

export const Header = () => {
    return (
        <header className="sticky top-0 z-50 w-full border-b border-surface-light bg-white/80 backdrop-blur-md px-6 md:px-10 py-3">
            <div className="max-w-[1440px] mx-auto flex items-center justify-between">
                <div className="flex items-center gap-8">
                    <div className="flex items-center gap-3 text-primary">
                        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white">
                            <span className="material-symbols-outlined text-2xl">grid_view</span>
                        </div>
                        <h2 className="text-neutral-dark text-lg font-bold leading-tight">
                            GPT-Md <span className="text-primary">Web</span>
                        </h2>
                    </div>
                    <nav className="hidden lg:flex items-center gap-8">
                        <a className="text-neutral-dark text-sm font-semibold border-b-2 border-primary pb-1" href="#">Dashboard</a>
                        <a className="text-neutral-gray text-sm font-medium hover:text-primary transition-colors" href="#">Templates</a>
                    </nav>
                </div>

                <div className="flex items-center gap-4">
                    <div className="hidden md:flex items-center bg-surface-light rounded-lg px-4 h-10 w-64">
                        <span className="material-symbols-outlined text-neutral-gray mr-2">search</span>
                        <input
                            className="bg-transparent border-none focus:ring-0 text-sm w-full placeholder:text-neutral-gray outline-none"
                            placeholder="Buscar propostas..."
                        />
                    </div>
                    <button className="bg-primary text-white text-sm font-bold h-10 px-4 rounded-lg hover:bg-blue-700 transition-colors whitespace-nowrap">
                        v12.5 stable
                    </button>
                    <div
                        className="w-10 h-10 rounded-full bg-slate-200 border-2 border-primary/20 flex items-center justify-center text-primary font-bold"
                    >
                        FB
                    </div>
                </div>
            </div>
        </header>
    );
};
