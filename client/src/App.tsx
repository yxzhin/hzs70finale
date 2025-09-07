import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import './App.css';

// Components
import Header from './components/Header';
import Footer from './components/Footer';

// Pages
import Hero from './pages/Hero';
import Dashboard from './pages/Dashboard';
import SignUpPage from './pages/SignUp';
import Information from './pages/Information';
import Invite from './pages/Invite';
import JoinGroup from './pages/JoinGroup';
import CreateGroup from './pages/CreateGroup';

// Logic
import SignUpRequest from './logic/SignUpRequests';
import LogInRequest from './logic/LogInRequests';
import Logout from './logic/Logout';
import CreateGroupFunc from './logic/CreateGroupFunc';

function App() {
    
    return (
        <div className="app">
            <BrowserRouter>
            <Header />
                <Routes>
                    <Route path="/" element={<Hero />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/signup" element={<SignUpPage />} />
                    <Route path="/signup" element={<SignUpPage />} />
                    <Route path="/info" element={<Information />} />
                    <Route path="/invite" element={<Invite />} />
                    <Route path="/join" element={<JoinGroup />} />
                    <Route path="/create_group" element={<CreateGroup />} />
                    <Route path="/sign_up_submit" element={<SignUpRequest />} />
                    <Route path="/log_in_submit" element={<LogInRequest />} />
                    <Route path="/logout" element={<Logout />} />
                    <Route path="/create_group_func" element={<CreateGroupFunc />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </BrowserRouter>
            <Footer />
        </div>
    );
}

export default App;