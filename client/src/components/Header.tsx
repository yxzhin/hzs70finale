import './Header.css';
import { useNavigate } from 'react-router-dom';

function Header () {
    const navigate = useNavigate();
    let text = "Get Started";
    let link = "/signup";
    let ComponentOnTheRight = <a href="/info" className='link header-info-link'>Information</a>;
    // This header can be used anywhere but the button text will change based on if the user is logged in or not (whether the user is on the dashboard or not)
    const token = localStorage.getItem('jwt');
    if (token) {
        text = "Log Out";
        link = "/logout";
        ComponentOnTheRight = <a href="/dashboard" className='link header-info-link'>Dashboard</a>;
    }

    const handleClick = (path: string) => {
        navigate(path);
    };

    // Idk what to do to the header on the information page if the user is logged in
    return (
        <header>
            <div className="lside-header">
                <h1 className='header-title'><span className='red-text'>Split</span>Smart</h1>
            </div>
            <div className="rside-header">
                {ComponentOnTheRight}
                <a href={link}>
                    <button 
                    className='primary-btn' 
                    onClick={() => handleClick(link)}
                >
                    {text}</button>
                </a>
            </div>
        </header>
    );
}

export default Header;