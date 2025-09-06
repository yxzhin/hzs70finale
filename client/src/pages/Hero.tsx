import './Hero.css';

import HeroSection from '../components/HeroSection';

function Hero() {
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