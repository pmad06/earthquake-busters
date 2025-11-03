import React, { useEffect, useState } from 'react';
import { EarthquakeMap } from './earthquakeMap';
import 'leaflet/dist/leaflet.css';

type Earthquake = {
  location: string;
  magnitude: number;
  lat: number;
  long: number;
  url: string;
};

export default function Home() {
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);

  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);
  const [magnitude, setMagnitude] = useState<number | null>(null);
  const [location, setLocation] = useState('');
  const [url, setURL] = useState('');
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
      <div style={{ display: 'flex', gap: '20px', marginTop: '20px', width: '1000px' }}>
        <div style={{ flex: 3 }}>
          <EarthquakeMap earthquakes={earthquakes} center={mapCenter} />
        </div>
        <div style ={{ 
          flex: 1,
          backgroundColor: 'white',
          border: '1px solid #ccc',
          borderRadius: '10px',
          color:'black', 
          textAlign: 'left', 
          padding: '10px',
          }}>
          <h3>Location: </h3>
            <p>{location}</p>
          <h3>Magnitude: </h3>
            <p>{magnitude}</p>
            <h3>More Info:</h3>
            <p style={{ wordBreak: 'break-word', overflowWrap: 'break-word' }}>
              <a href={url} target="_blank" rel="noreferrer">{url}</a>
            </p>        
         </div>
      </div>     

      <div style={{ marginTop: '20px', marginRight: '220px' }}>
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
               
              // Find earthquake matching entered lat/lng
              const match = earthquakes.find((q) =>
                  Math.abs(q.lat - latitude) < 0.01 &&
                  Math.abs(q.long - longitude) < 0.01
              );

              if (match) {
                setLocation(match.location);
                setMagnitude(match.magnitude);
                setURL(match.url);
              } 
            }
          }}
          >
            Move Map
          </button>
        </div>
    </div>
  );
}
