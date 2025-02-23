"use client";

import { useState } from "react";
import { supabase } from "@/lib/supabase";
import { useRouter } from "next/navigation";
import Link from 'next/link';


export default function AuthPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleSignUp = async () => {
    const { error } = await supabase.auth.signUp({ email, password });
    if (!error) {
      alert("Check your email for confirmation!");
    }
  };

  const handleSignIn = async () => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (!error) {
      router.push("/dashboard"); // Redirect to the dashboard
    }
  };

  return (
    <main className="login-page">
      <section className="login-form">
        <header className="logo">
        <div>
            <img src="/images/logo.png" alt="Logo" id="logo" />
        </div>          
          <h1>Body Cam</h1>
        </header>
        <div className="form-container">
          <h2>Login / Sign Up</h2>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button className="login-button" onClick={handleSignUp}>Sign Up</button>
          <button className="login-button" onClick={handleSignIn}>Login</button>
          <Link href="/submitComplaint" passHref>
            <button className="complaint-button" style={{ textDecoration: "none" }}>
                Submit a Complaint
            </button>
            </Link>

        </div>
      </section>

      <section className="globe-section">
        <div className="globe-container">
            <img src="/images/globe.png" alt="Globe" id="globe" />
        </div>
      </section>
    </main>
  );
}
