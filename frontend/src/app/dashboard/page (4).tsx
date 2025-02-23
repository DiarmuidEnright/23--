import React from 'react';
import Link from 'next/link';
import MapView from './MapView';
import Navbar from './Navbar';
import { useState, useEffect } from 'react';

function DashboardPage() {
    return (
      <div>
        <Navbar />
        <MapView />
        
        <Link href="/about">
          About Us
        </Link>
      </div>

  );
}

export default DashboardPage;
