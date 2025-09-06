import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import './SignUp.css';

function SignUpPage() {
    const navigate = useNavigate();

    let [signupClass, setSignupClass] = useState('text-activated');
    let [loginClass, setLoginClass] = useState('');

    const [formData, setFormData] = useState({
        name: "",
        password: "",
        passwordConfirm: ""
    });

    const [toDisplayClass, setToDisplayClass] = useState(true);

    const [toNavigateTo, setToNavigateTo] = useState('/sign_up_submit');

    const signupClick = () => {
        setSignupClass('text-activated');
        setLoginClass('');
        setToDisplayClass(true);
        setToNavigateTo('/sign_up_submit');
    }

    const loginClick = () => {
        setSignupClass('');
        setLoginClass('text-activated');
        setToDisplayClass(false);
        setToNavigateTo('/log_in_submit');
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }));
    };

    const handleSubmitSignup = (e: React.FormEvent) => {
        e.preventDefault();
        
        navigate(toNavigateTo, { state: formData });
    };

    return (
        <div className="signup-page">
            <div className="form">
                <div className="signup-texts">
                    <h1 className={signupClass} onClick={signupClick}>Sign Up</h1>
                    <h1 className={loginClass} onClick={loginClick}>Log in</h1>
                </div>

                <form className='signup-form' onSubmit={handleSubmitSignup}>
                    <input
                        type='text'
                        name='name'
                        placeholder='Enter your name'
                        required
                        value={formData.name}
                        onChange={handleChange}
                    />
                    <input
                        type='password'
                        name='password'
                        placeholder='Enter your password'
                        required
                        value={formData.password}
                        onChange={handleChange}
                    />
                    {toDisplayClass ? <input
                        type='password'
                        name='passwordConfirm'
                        placeholder='Confirm your password'
                        required
                        value={formData.passwordConfirm}
                        onChange={handleChange}
                    /> : null}
                    <button type='submit' className='submit-btn'>Sign up</button>
                </form>
            </div>
        </div>
    );
}

export default SignUpPage;