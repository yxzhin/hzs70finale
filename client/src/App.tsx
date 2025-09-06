import { BrowserRouter, Routes, Route } from 'react-router-dom';

import './App.css';

// Components
import Header from './components/Header';
import Footer from './components/Footer';

// Pages
import Hero from './pages/Hero';
import Dashboard from './pages/Dashboard';

function App() {
    
    return (
        <div className="app">
            <Header />

            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Hero />} />
                    <Route path="/Dashboard" element={<Dashboard />} />
                </Routes>
            </BrowserRouter>
            <Footer />
        </div>
    );
}

export default App;