import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import { BrowserRouter } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';


const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

ReactDOM.createRoot(document.getElementById('root')).render( 
  <React.StrictMode>
    <GoogleOAuthProvider clientId={googleClientId}> {/* 추가 */}
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </GoogleOAuthProvider> {/* 추가 */}
  </React.StrictMode>,
);