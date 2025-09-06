import './Header.css';

function Header () {
    let text = "Get Started";
    let link = "/signup";
    // This header can be used anywhere but the button text will change based on if the user is logged in or not (whether the user is on the dashboard or not)
    const token = localStorage.getItem('jwt');
    if (token) {
        text = "Log Out";
        link = "/logout";
    }
    // Need to add the drop down menu for the dashboard view. Needs several returns based on if the user is logged in or not
    return (
        <header>
            <div className="lside-header">
                <h1 className='header-title'><span className='red-text'>Split</span>Smart</h1>
            </div>
            <div className="rside-header">
                <a href="/info" className='link header-info-link'>Information</a>
                <a href={link}>
                    <button className='primary-btn'>{text}</button>
                </a>
            </div>
        </header>
    );
}

export default Header;