import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <Link to="/">
            <img src="https://media.discordapp.net/attachments/1436081196634341396/1437038720741146655/image.png?ex=6911ca19&is=69107899&hm=dd885fd0150bed07e76022ca25822b4384202ef56705979b20a63e0fe5ef3d8e&=&format=webp&quality=lossless&width=1076&height=528" alt="Avatar Exchange Logo" className="navbar-logo" />
          </Link>
        </div>

        
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
              to="/portfolio" 
              className={`navbar-link ${location.pathname === '/portfolio' ? 'active' : ''}`}
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
      </div>
    </nav>
  );
};

export default Navbar;