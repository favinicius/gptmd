import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Bot, FileText, History, Settings, ExternalLink } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

const SidebarItem = ({ icon: Icon, label, path }) => {
    const location = useLocation();
    const isActive = location.pathname === path;

    return (
        <Link
            to={path}
            className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-sm font-medium",
                isActive
                    ? "bg-blue-600 text-white shadow-md"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
            )}
        >
            <Icon size={20} />
            <span>{label}</span>
            {isActive && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-white" />}
        </Link>
    );
};

const Layout = ({ children }) => {
    return (
        <div className="flex h-screen bg-slate-50 font-sans">
            {/* Sidebar */}
            <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
                <div className="p-6 border-b border-slate-100 flex items-center gap-2">
                    <div className="bg-blue-600 p-2 rounded-lg">
                        <Bot className="text-white" size={24} />
                    </div>
                    <div>
                        <h1 className="font-bold text-lg text-slate-800 tracking-tight">GPT-Md</h1>
                        <span className="text-xs text-slate-400 font-mono">v12.5 Web</span>
                    </div>
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4 px-4 mt-2">
                        Menu
                    </div>
                    <SidebarItem icon={FileText} label="Nova Proposta" path="/" />
                    <SidebarItem icon={History} label="Histórico" path="/history" />
                    <SidebarItem icon={Settings} label="Configurações" path="/settings" />
                </nav>

                <div className="p-4 border-t border-slate-100">
                    <a href="https://github.com/favinicius/gptmd" target="_blank" className="flex items-center gap-2 text-xs text-slate-400 hover:text-blue-600 transition-colors px-4">
                        <ExternalLink size={14} />
                        <span>Documentação</span>
                    </a>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-auto">
                <div className="max-w-7xl mx-auto p-8">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
