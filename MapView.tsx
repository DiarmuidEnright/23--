"use client";

import React, { useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L, { Icon } from 'leaflet';
import customIcon from './custom-marker.png';
import FetchData from '@/fetchData';


function MapView() {
  const [position2, setPosition3] = useState<[number, number]>([-0.20, 40]);
  const [position, setPosition1] = useState<[number, number]>([51.505, -0.09]);
  const [position1, setPosition2] = useState<[number, number]>([53.3492832, -6.2476664]);
  const markerRef = useRef<any>(null);

  const myIcon: Icon = new L.Icon({
    iconUrl: './images/custom-marker.png',
    iconSize: [38, 38],
  });

  const myIcon1: Icon = new L.Icon({
    iconUrl: './images/custom-marker.png',
    iconSize: [38, 38],
  });

  const myIcon2: Icon = new L.Icon({
    iconUrl: './images/custom-marker.png',
    iconSize: [38, 38],
  });

  const description = "Summary of events: Act of physical violence - a gun was pulled on the police officer at time stamp: 12.34 in the body camera footage.";
  const containsSensitiveWord = description.toLowerCase().includes("violence") || description.toLowerCase().includes("aggression");
  const containsSecondarySensitiveWord = description.toLowerCase().includes("angry") || description.toLowerCase().includes("shouting");




  return (
    <div style={{ position: 'relative' }}>

      {/* Map Section */}
      <MapContainer
        center={position}
        zoom={13}
        scrollWheelZoom={true}
        style={{ height: '100vh', width: '120%' }}
        maxBounds={[
          [-90, -180], // Southwest coordinates
          [90, 180],   // Northeast coordinates
        ]}
        minZoom={2}   // Prevents zooming out too far
        maxZoom={18}
        maxBoundsViscosity={1.0} 
      >



        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />



        <Marker
          position={position}
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


        <Marker
          position={position1}
          icon={myIcon1}
          ref={markerRef}
        >
          <Popup maxWidth={400}>
            <h3>BodyCam footage</h3>
            <hr />
            <video width="100%" height="215" controls>
              <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <p>DogPatch Labs</p>
            📍 Location: <strong>{position1[0]}, {position1[1]}</strong>
          </Popup>
        </Marker>

        <Marker
          position={position2}
          icon={myIcon2}
          ref={markerRef}
        >
          <Popup maxWidth={400}>
            <h3>BodyCam footage</h3>
            <hr />
            <iframe width="400" height="250" src="https://www.youtube.com/embed/hICeE4PKEYg?si=HaPrhrdTrsE54Dri" title="YouTube video player" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"></iframe>
            <FetchData/>
            📍 Location: <strong>{position2[0]}, {position2[1]}</strong>
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
