"use client";

import { useState } from "react";

const SubmitComplaint = () => {
  // State for form fields
  const [formData, setFormData] = useState({
    full_name: "",
    country: "",
    city: "",
    summary: "",
  });

  const [message, setMessage] = useState("");

  // Function to handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Function to handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const response = await fetch("https://evxchpvtxienefjtcbhs.supabase.co/rest/v1/complaints", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV2eGNocHZ0eGllbmVmanRjYmhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAyNDUzMTMsImV4cCI6MjA1NTgyMTMxM30.AT95PWkDSPUBQAQCmE1VZrhIltvOuj4moE34pRs3OVw", // Replace with your actual key
        "Authorization": `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV2eGNocHZ0eGllbmVmanRjYmhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAyNDUzMTMsImV4cCI6MjA1NTgyMTMxM30.AT95PWkDSPUBQAQCmE1VZrhIltvOuj4moE34pRs3OVw`, // Replace with your actual key
      },
      
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      setMessage("Complaint submitted successfully!");
      setFormData({ full_name: "", country: "", city: "", summary: "" }); // Clear form
    } else {
      setMessage("Error submitting complaint. Please try again.");
    }
  };

  return (
    <div className="complaint-form-container">
      <h2>Submit a Complaint</h2>
      <form onSubmit={handleSubmit} className="complaint-form">
        <input
          type="text"
          name="full_name"
          placeholder="Full Name"
          value={formData.full_name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="country"
          placeholder="Country"
          value={formData.country}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="city"
          placeholder="City"
          value={formData.city}
          onChange={handleChange}
          required
        />
        <textarea
          name="summary"
          placeholder="Description of Incident"
          value={formData.summary}
          onChange={handleChange}
          required
        />
        <button type="submit" className="submit-button">Submit</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default SubmitComplaint;
