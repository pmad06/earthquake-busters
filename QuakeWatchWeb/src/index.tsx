import React, { useEffect, useState } from 'react';
import { EarthquakeMap } from './earthquakeMap';
import 'leaflet/dist/leaflet.css';

type Earthquake = {
  title: string;
  magnitude: number;
  latitude: number;
  longitude: number;
};

export default function Home() {
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);

  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);
  const [mapCenter, setMapCenter] = useState<[number, number]>([37.7749, -122.4194]);
 
  useEffect(() => {
    fetch('http://127.0.0.1:5000/earthquakes')
      .then(res => res.json())
      .then(data => setEarthquakes(data))
      .catch(err => console.error(err));
  }, []);


  return (
    <div>
      <h1>Earthquake Map</h1>
      <EarthquakeMap earthquakes={earthquakes} center = {mapCenter}/>


      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <input
          type="number"
          placeholder="Latitude"
          value={latitude !== null ? latitude : ''}
          onChange={(e) => setLatitude(e.target.value ? parseFloat(e.target.value) : null)}
          style={{
            padding: '8px',
            marginRight: '10px',
          }}
          />
        <input
          type="number"
          placeholder="Longitude"
          value={longitude !== null ? longitude : ''}
          onChange={(e) => setLongitude(e.target.value ? parseFloat(e.target.value) : null)}
          style={{
            padding: '8px',
            marginRight: '10px',
          }}
        />
        <button
          onClick={() => {
            if (latitude !== null && longitude !== null) {
              setMapCenter([latitude, longitude]);
            }
          }}
          >
            Move Map
          </button>
        </div>
    </div>
  );
}
