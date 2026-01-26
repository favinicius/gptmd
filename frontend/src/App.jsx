import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';

function App() {
    return (
        <BrowserRouter>
            <Layout>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/history" element={<div className="text-slate-500">Histórico em construção...</div>} />
                    <Route path="/settings" element={<div className="text-slate-500">Configurações em construção...</div>} />
                </Routes>
            </Layout>
        </BrowserRouter>
    );
}

export default App;
