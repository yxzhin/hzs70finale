import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

import './Hero.css';

import HeroSection from '../components/HeroSection';

function Hero() {
    const navigate = useNavigate();

    // Attempt to log in with a JWT token
    const token = localStorage.getItem('jwt');
    if (token) {
        const hasFetched = useRef(false);
        
        useEffect(() => {
            if (hasFetched.current) return;
            hasFetched.current = true;
        
            fetch("http://localhost:5000/user/current_user", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            })
            .then(async (res) => {
                if (res.status == 404) {
                    return;
                } else if (res.status == 500) {
                    localStorage.setItem('jwt', '');
                    window.location.reload();
                } else if (res.status == 200) {
                    const result = await res.json();
                    console.log("Server response:", result);
                    navigate("/dashboard", { replace: true });
                } else {
                    throw new Error(`Unexpected status: ${res.status}`);
                }
            })
            .catch(err => {
                console.error("Registration error:", err);
                navigate("/signup?error=server", { replace: true });
            });
        }, [token, navigate]);
    }

    return (
        <div className="hero">
            <div className="hero-sec">
                <div className="lside-hero">
                    <h1 className="hero-title">
                        Split <span className="red-text">Bills</span>,<br />
                        Not <span className="red-text">Friendships</span>
                    </h1>

                    <p className='hero-subtitle'>
                        Smart, stress-free expense sharing for roommates and friends
                    </p>

                    <div className="hero-btns">
                        <a href="/signup">
                            <button className="primary-btn hero-cta-btn">Get Started</button>
                        </a>

                        <a href="/info" className="link hero-info-link">or see how it works</a>
                    </div>
                </div>

                <div className="rside-hero">
                    <img src='/hero-img.png' alt='Hero' className='hero-img' />
                </div>
            </div>

            <HeroSection
                title={<h1 className='hero-sec-title'>No more awkward <span className='red-text'>IOU</span>-s</h1>}
                description={<p className='hero-sec-subtitle'>Stop chasing friends for money -
                    <span className='red-text'> Split</span>Smart 
                    keeps everything transparent and fair.</p>
                    
                }
                imageSrc='IOU.png'
            />

            <HeroSection
                title={<h1 className='hero-sec-title'><span className='red-text'>Fair</span> splits, always</h1>}
                description={<p className='hero-sec-subtitle'>Log bills quickly and let the app do the math for you.</p>}
                imageSrc='notes.png'
            />

            <HeroSection
                title={<h1 className='hero-sec-title'>Track <span className='red-text'>expenses</span> in seconds</h1>}
                description={<p className='hero-sec-subtitle'>From equal shares to custom splits, everyone pays their fair part.</p>}
                imageSrc='equalizer.png'
            />
        </div>
    );
}

export default Hero;