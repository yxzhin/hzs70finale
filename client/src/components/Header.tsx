import './Header.css';

function Header () {
    return (
        <header>
            <div className="lside-header">
                <h1 className='header-title'><span className='red-text'>Split</span>Smart</h1>
            </div>

            <div className="rside-header">
                <a href="/info" className='link header-info-link'>Information</a>
                <a href="/signup">
                    <button className='primary-btn'>Get Started</button>
                </a>
            </div>
        </header>
    );
}

export default Header;