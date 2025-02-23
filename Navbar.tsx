import React from 'react';
import Link from 'next/link';

function Navbar() {
  return (
    <nav className="navbar">
    
      <div className="navbar_container">
        <Link href="/" id="navbar_logo" passHref>BodyCam</Link>
        <div className="navbar_toggle" id="mobile-menu">
          <span className="bar"></span>
          <span className="bar"></span>
          <span className="bar"></span>
        </div>
      </div>
      <ul className="navbar_menu">
        <li className="navbar_item"><Link href="/dashboard" className="navbar_links" passHref>Home</Link></li>
        <li className="navbar_item"><Link href="/complaints" className="navbar_links" passHref>Complaints</Link></li>
        <li className="navbar_item"><Link href="/about" className="navbar_links" passHref>About</Link></li>
        <li className="navbar_item"><Link href="/contact" className="navbar_links" passHref>Contact Us</Link></li>
        <li className="navbar_btn"><Link href="/auth" className="button" passHref>Sign Out</Link></li>
      </ul>
    </nav>
    
  );
}

export default Navbar;