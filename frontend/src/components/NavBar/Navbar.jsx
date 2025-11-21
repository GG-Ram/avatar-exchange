import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useUser } from '../../Hooks/userContext';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, userInfo, logout, user } = useUser();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <Link to="/market">
            <img src="https://media.discordapp.net/attachments/1436081196634341396/1437038720741146655/image.png?ex=6911ca19&is=69107899&hm=dd885fd0150bed07e76022ca25822b4384202ef56705979b20a63e0fe5ef3d8e&=&format=webp&quality=lossless&width=1076&height=528" alt="Avatar Exchange Logo" className="navbar-logo" />
          </Link>
        </div>

        
        {isAuthenticated ? (
          <>
            <ul className="navbar-menu">
              <li className="navbar-item">
                <Link 
                  to="/market" 
                  className={`navbar-link ${location.pathname === '/market' ? 'active' : ''}`}
                >
                  <span className="icon">📈</span>
                  <span>Market</span>
                </Link>
              </li>

              <li className="navbar-item">
                <Link 
                  to="/Portfolio" 
                  className={`navbar-link ${location.pathname === '/Portfolio' ? 'active' : ''}`}
                >
                  <span className="icon">💼</span>
                  <span>Portfolio</span>
                </Link>
              </li>
              
              <li className="navbar-item">
                <Link 
                  to="/shop" 
                  className={`navbar-link ${location.pathname === '/shop' ? 'active' : ''}`}
                >
                  <span className="icon">🏪</span>
                  <span>Shop</span>
                </Link>
              </li>
              
              <li className="navbar-item">
                <Link 
                  to="/avatar" 
                  className={`navbar-link ${location.pathname === '/avatar' ? 'active' : ''}`}
                >
                  <span className="icon">👤</span>
                  <span>Avatar</span>
                </Link>
              </li>
            </ul>
            
            <div className="navbar-user">
              <div className="user-info">
                <span className="username">{userInfo?.username}</span>
                {user && <span className="balance">${user.balance?.toFixed(2) || '0.00'}</span>}
              </div>
              <button onClick={handleLogout} className="logout-button">
                Logout
              </button>
            </div>
          </>
        ) : (
          <div className="navbar-auth">
            <Link to="/login" className="auth-link">
              Login
            </Link>
            <Link to="/register" className="auth-link register-link">
              Register
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;