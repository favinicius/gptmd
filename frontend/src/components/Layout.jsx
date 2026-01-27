import React from 'react';
import { Header } from './ds/Header';
import { Sidebar } from './ds/Sidebar';
import { twMerge } from 'tailwind-merge';
import { clsx } from 'clsx';

export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

const Layout = ({ children }) => {
    return (
        <div className="flex flex-col min-h-screen bg-background-light font-sans text-neutral-dark">
            <Header />
            <div className="flex flex-1 relative">
                <Sidebar />
                <main className="flex-1 w-full overflow-x-hidden">
                    <div className="max-w-[1200px] mx-auto p-6 md:p-10">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};

export default Layout;
