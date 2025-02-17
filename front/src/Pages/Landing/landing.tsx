import { useState } from 'react';

// CSS
import './landing.css';

// Components
import Register from '../../Components/Register/register';

function Landing () {

    // States
    const [isRegisterOpen, setIsRegisterOpen] = useState(false);

    return (
        <div className='landing-wrapper'>
            <div className='landing-title-wrapper'>
                <span className='landing-title'> Love Awaits </span>
            </div>

            <div className='landing-register-button-wrapper'>
                <button className='landing-register-button' onClick={() => setIsRegisterOpen(true)}> Create account </button>
            </div>

            {isRegisterOpen && (
                <>
                    <div className="overlay"></div>
                    <Register isRegisterOpen={isRegisterOpen} setIsRegisterOpen={setIsRegisterOpen}/>
                </>
            )}
        </div>
    );
}

export default Landing;