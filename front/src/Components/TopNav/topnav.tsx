import { useState } from 'react';

// CSS
import './topnav.css';

// Images
import snaplove_logo from '../../Assets/Images/SnapLove_Logo.png'

// Components
import Login from '../Login/login';

function TopNav () {

    const [isLoginOpen, setIsLoginOpen] = useState(false);

    return (
        <div className='topnav-wrapper'>
            <div className='topnav-logo-wrapper'>
                <img src={snaplove_logo} alt="Tinder Logo" className='topnav-logo' />
            </div>

            <div className='topnav-login-button-wrapper'>
                <button className='topnav-login-button' onClick={() => setIsLoginOpen(true)}> Log in </button>
            </div>

            {isLoginOpen && (
                <>
                    <div className="overlay"></div>
                    <Login isLoginOpen={isLoginOpen} setIsLoginOpen={setIsLoginOpen} />
                </>
            )}
        </div>
    );
}

export default TopNav;