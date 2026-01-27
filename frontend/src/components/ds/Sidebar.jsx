import React from 'react';
import { NavLink } from 'react-router-dom';

export const Sidebar = () => {
    const menuSections = [
        {
            title: 'Principais',
            items: [
                { icon: 'post_add', label: 'Nova Proposta', href: '/' },
                { icon: 'database', label: 'Base de Dados', href: '/registers' },
                { icon: 'history', label: 'Histórico', href: '/history' },
            ]
        },
        {
            title: 'Sistema',
            items: [
                { icon: 'settings', label: 'Configurações', href: '/settings' },
                { icon: 'help', label: 'Ajuda', href: '/help' }
            ]
        }
    ];

    return (
        <aside className="w-64 hidden md:flex flex-col border-r border-surface-light p-6 gap-8 sticky top-[65px] h-[calc(100vh-65px)] overflow-y-auto bg-white">
            {menuSections.map((section, idx) => (
                <div key={idx} className="flex flex-col gap-2">
                    <h3 className="text-[11px] font-bold text-neutral-gray uppercase tracking-widest px-3">
                        {section.title}
                    </h3>
                    {section.items.map((item, itemIdx) => (
                        <NavLink
                            key={itemIdx}
                            to={item.href}
                            className={({ isActive }) => `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${isActive
                                ? 'bg-primary/10 text-primary font-semibold'
                                : 'text-neutral-gray hover:bg-gray-100'
                                }`}
                        >
                            <span className="material-symbols-outlined !text-[20px]">{item.icon}</span>
                            {item.label}
                        </NavLink>
                    ))}
                </div>
            ))}

            <div className="mt-auto pt-6 border-t border-surface-light">
                <div className="bg-background-light p-4 rounded-xl">
                    <p className="text-xs font-bold text-neutral-dark mb-1">Preciso de ajuda?</p>
                    <p className="text-[11px] text-neutral-gray leading-relaxed">
                        Consulte a documentação técnica no repositório.
                    </p>
                </div>
            </div>
        </aside>
    );
};
