import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { GoogleOAuthProvider } from "@react-oauth/google"

// Components
import { ThemeProvider } from './Components/Theme/ThemeContext';

// Global Veribales
import { GOOGLE_CLIENT_ID } from './Assets/GlobalVeriables';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
  <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID!}>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </GoogleOAuthProvider>

);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
