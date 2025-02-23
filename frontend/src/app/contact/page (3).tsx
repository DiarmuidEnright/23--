import React from "react";
import Link from "next/link";
import Image from "next/image";
import Navbar from "../dashboard/Navbar";

function ContactPage() {
  return (
    <div>
      {/* Main Container */}
      <Navbar/>
      <div className="main">
        <div className="main_container">
          <div className="main_content">
            <h1>Contact Us</h1>
            <p>Email: BodyCam123@gmail.com</p>
            <p>Phone number: +353XXXXXXX</p>
          </div>

          <div className="main_img--container">
            <Image src="/images/contact.jpg" alt="Contact Image" width={500} height={300} />
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="footer_container">
        <div className="footer_links">
          <div className="footer_link-wrapper">
            <div className="footer_link-items">
              <h2>About Us</h2>
              <ul>
                <li>
                  <Link href="/about">Information Page</Link>
                </li>
              </ul>
            </div>

            <div className="footer_link-items">
              <h2>Contact</h2>
              <ul>
                <li>
                  <Link href="/contact">How to contact us</Link>
                </li>
              </ul>
            </div>

            <div className="footer_link-items">
              <h2>Social Media</h2>
              <ul>
                <li>
                  <a href="/">LinkedIn</a>
                </li>
                <li>
                  <a href="/">Instagram</a>
                </li>
                <li>
                  <a href="/">Facebook</a>
                </li>
                <li>
                  <a href="/">YouTube</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ContactPage;
