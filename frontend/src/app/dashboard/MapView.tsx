import React, { useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L, { Icon } from 'leaflet';
import customIcon from '../components/custom-marker.png';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

function MapView() {
  const [position, setPosition] = useState<[number, number]>([51.505, -0.09]);
  const [lat, setLat] = useState<string>(position[0].toString());
  const [lng, setLng] = useState<string>(position[1].toString());
  const [error, setError] = useState<string>('');
  const markerRef = useRef<any>(null);

  const myIcon: Icon = new L.Icon({
    iconUrl: customIcon as string,
    iconSize: [38, 38],
  });

  const description = "Summary of events: Act of physical violence - a gun was pulled on the police officer at time stamp: 12.34 in the body camera footage.";
  const containsSensitiveWord = description.toLowerCase().includes("violence") || description.toLowerCase().includes("aggression");
  const containsSecondarySensitiveWord = description.toLowerCase().includes("angry") || description.toLowerCase().includes("shouting");


  const handleUpdatePosition = () => {
    const latitude = parseFloat(lat);
    const longitude = parseFloat(lng);

    if (isNaN(latitude) || isNaN(longitude)) {
      setError('❌ Please enter valid numeric values for latitude and longitude.');
      return;
    }
    if (latitude < -90 || latitude > 90 || longitude < -180 || longitude > 180) {
      setError('⚠️ Latitude must be between -90 and 90, and longitude between -180 and 180.');
      return;
    }

    setPosition([latitude, longitude]);
    setError('');
  };

  const handleMarkerDragEnd = () => {
    const marker = markerRef.current;
    if (marker != null) {
      const { lat, lng } = marker.getLatLng();
      setPosition([lat, lng]);
      setLat(lat.toFixed(6));
      setLng(lng.toFixed(6));
    }
  };

  return (
    <div style={{ position: 'relative' }}>
      {/*  Floating Input Section */}
      <div
        style={{
          position: 'absolute',
          top: '10px',
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: '12px',
          padding: '1rem 2rem',
          backdropFilter: 'blur(10px)',
          backgroundColor: 'rgba(0, 0, 0, 0.3)',
          borderRadius: '16px',
          boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
          zIndex: 1000,
        }}
      >



        <input
          type="text"
          placeholder="Latitude"
          value={lat}
          onChange={(e) => setLat(e.target.value)}
          style={{
            padding: '0.5rem',
            width: '150px',
            border: 'none',
            borderBottom: '2px solid #00f2ff',
            outline: 'none',
            backgroundColor: 'transparent',
            color: '#ffffff',
            fontSize: '1rem',
          }}
        />



        <input
          type="text"
          placeholder="Longitude"
          value={lng}
          onChange={(e) => setLng(e.target.value)}
          style={{
            padding: '0.5rem',
            width: '150px',
            border: 'none',
            borderBottom: '2px solid #00f2ff',
            outline: 'none',
            backgroundColor: 'transparent',
            color: '#ffffff',
            fontSize: '1rem',
          }}
        />


        <button
          onClick={handleUpdatePosition}
          style={{
            padding: '0.5rem 1.5rem',
            borderRadius: '8px',
            border: 'none',
            backgroundColor: '#00f2ff',
            color: '#000000',
            fontWeight: 'bold',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
          }}
        >



          Update Marker 📍
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <p style={{ color: 'red', textAlign: 'center', fontWeight: 'bold', marginTop: '80px' }}>
          {error}
        </p>
      )}

      {/* Map Section */}
      <MapContainer
        center={position}
        zoom={13}
        scrollWheelZoom={true}
        style={{ height: '120vh', width: '120%' }}
      >



        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />



        <Marker
          position={position}
          draggable={true}
          eventHandlers={{
            dragend: handleMarkerDragEnd,
          }}
          icon={myIcon}
          ref={markerRef}
        >



          <Popup maxWidth={400}>
            <h3>BodyCam footage</h3>
            <hr />
            <video width="100%" height="215" controls>
              <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <p>{description}</p>
            📍 Location: <strong>{position[0]}, {position[1]}</strong>
          </Popup>
        </Marker>
        {/*Conditionally rendered - might add a second condition*/}
        {containsSensitiveWord && (
          <Circle
            center={position}
            radius={500} // 500 meters radius
            pathOptions={{ color: 'red', fillColor: 'red', fillOpacity: 0.3 }}
          />
        )}

      {containsSecondarySensitiveWord && (
          <Circle
            center={position}
            radius={500} // 500 meters radius
            pathOptions={{ color: 'orange', fillColor: 'red', fillOpacity: 0.3 }}
          />
        )}  
      </MapContainer>
    </div>
  );
}

export default MapView;
