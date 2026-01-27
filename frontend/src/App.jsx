import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import NewProposal from './pages/NewProposal';
import ProposalWizard from './pages/ProposalWizard';
import History from './pages/History';
import BaseRegisters from './pages/BaseRegisters';

function App() {
    return (
        <BrowserRouter>
            <Layout>
                <Routes>
                    <Route path="/" element={<ProposalWizard />} />
                    <Route path="/legacy-new" element={<NewProposal />} />
                    <Route path="/registers" element={<BaseRegisters />} />
                    <Route path="/history" element={<History />} />
                    <Route path="/settings" element={<div className="text-slate-500">Configurações em construção...</div>} />
                </Routes>
            </Layout>
        </BrowserRouter>
    );
}

export default App;
