import Link from 'next/link';
import React from 'react';

function AboutPage() {
  return (
    <div>
      <div className="main">
        <div className="main_container">
          <div className="main_content">
            <h1>About Us</h1>
            <p>Learn all about our goals!</p>
          </div>
          <div className="main_img--container">
            <img src="images/23.jpg" alt="images/23.jpg" id="main_img" />
          </div>
        </div>
      </div>

      <div className="services2">
        <h1>Our Mission</h1>
        <div className="services_container_about">
          <h2>
            Here at BodyCam, our goal is to analyse body camera footage so that we can reduce the 930 terabytes of video feed stored by the US police force each year to only the essential moments where aggression or violence are noted by AI, then noted and kept for review.
          </h2>
          <p>Thank you for taking the time to learn about us!</p>
        </div>
      </div>

      <div className="footer_container">
        <div className="footer_links">
          <div className="footer_link-wrapper">
            <div className="footer_link-items">
              <h2>About Us</h2>
              <li>
                <Link href="/about">Information Page</Link>
              </li>
            </div>
            <div className="footer_link-items">
              <h2>Contact</h2>
              <li>
                <Link href="/contact">How to contact us</Link>
              </li>
            </div>
            <div className="footer_link-items">
              <h2>Social Media</h2>
              <a href="/">LinkedIn</a>
              <a href="/">Instagram</a>
              <a href="/">Facebook</a>
              <a href="/">Youtube</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AboutPage;