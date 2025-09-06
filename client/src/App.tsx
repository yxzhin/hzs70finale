import { BrowserRouter, Routes, Route } from 'react-router-dom';

import './App.css';

// Components
import Header from './components/Header';
import Footer from './components/Header';

// Pages
import Hero from './pages/Hero';

function App() {
    return (
        <div className="app">
            <Header />

            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Hero />} />
                </Routes>
            </BrowserRouter>
            <Footer />
        </div>
    );
}

export default App;