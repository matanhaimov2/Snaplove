// CSS
import './pageLoader.css';

// Images
import snap_icon from '../../../Assets/Images/SnapLove_Icon.png'

function PageLoader() {

    return (
        <div className='pageLoader-wrapper'>
            <img className='pageLoader-img' src={snap_icon}></img>
        </div>
    );
}

export default PageLoader;