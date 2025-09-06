import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import './App.css';

// Components
import Header from './components/Header';
import Footer from './components/Footer';

// Pages
import Hero from './pages/Hero';
import SignUpPage from './pages/SignUp';

// Logic
import SignUpRequest from './logic/SignUpRequests';

function App() {
    return (
        <div className="app">
            <Header />

            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Hero />} />
                    <Route path="/signup" element={<SignUpPage />} />
                    <Route path="/sign_up_submit" element={<SignUpRequest />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </BrowserRouter>
            <Footer />
        </div>
    );
}

export default App;