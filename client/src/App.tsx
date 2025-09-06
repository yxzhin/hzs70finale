import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import './App.css';

// Components
import Header from './components/Header';
import Footer from './components/Footer';

// Pages
import Hero from './pages/Hero';
import SignUpPage from './pages/SignUp';
import Information from './pages/Information';
import Success from './pages/Success';

// Logic
import SignUpRequest from './logic/SignUpRequests';
import LogInRequest from './logic/LogInRequests';

function App() {
    return (
        <div className="app">
            <Header />

            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Hero />} />
                    <Route path="/signup" element={<SignUpPage />} />
                    <Route path="/signup" element={<SignUpPage />} />
                    <Route path="/info" element={<Information />} />
                    <Route path="/success" element={<Success />} />
                    <Route path="/sign_up_submit" element={<SignUpRequest />} />
                    <Route path="/log_in_submit" element={<LogInRequest />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </BrowserRouter>
            <Footer />
        </div>
    );
}

export default App;