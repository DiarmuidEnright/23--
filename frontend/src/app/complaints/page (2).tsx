"use client";
import React, { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";
import Navbar from '../dashboard/Navbar';

// Supabase Configuration
const supabase = createClient(
  "https://evxchpvtxienefjtcbhs.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV2eGNocHZ0eGllbmVmanRjYmhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAyNDUzMTMsImV4cCI6MjA1NTgyMTMxM30.AT95PWkDSPUBQAQCmE1VZrhIltvOuj4moE34pRs3OVw"
);

interface Complaint {
  id: number;
  full_name: string;
  country: string;
  city: string;
  summary: string;
}

const ComplaintsPage = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchComplaints() {
      const { data, error } = await supabase.from("complaints").select("*");
      if (error) {
        setError(error.message);
      } else {
        setComplaints(data);
      }
    }
    fetchComplaints();
  }, []);

  return (
    <div className="complaints-container">
      <Navbar />;
      <h1 className="page-title">Live Complaints</h1>
      {error && <p className="error-message">{error}</p>}

      <table className="complaints-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Country</th>
            <th>City</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {complaints.map((complaint) => (
            <tr key={complaint.id}>
              <td>{complaint.id}</td>
              <td>{complaint.full_name}</td>
              <td>{complaint.country}</td>
              <td>{complaint.city}</td>
              <td>{complaint.summary}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ComplaintsPage;
