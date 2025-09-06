import './Hero.css';

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
        </div>
    );
}

export default Hero;