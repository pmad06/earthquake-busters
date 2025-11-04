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

  //const [trieCount, setTrieCount] = useState<number>(0);

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
      // .then(data => {
      //   setEarthquakes(data.splay_sorted);
      //   setTrieCount(data.total_stored_in_trie);
      // })
      .catch(err => console.error(err));
  }, []);

  return (
    <div id = "homepage">
      <h1>Earthquake Map</h1>
      <div style={{ display: 'flex', gap: '20px', marginTop: '20px', width: '1000px' }}>
        <div style={{ flex: 3 }}>
          <EarthquakeMap earthquakes={earthquakes} center={mapCenter} />
        </div>
        <div id = "sidebar" style ={{ flex: 1}}>
          <h3>Location: </h3>
            <p className = 'answers'>{location}</p>
          <h3>Latitude: </h3>
            <p className = 'answers'>{latitude}</p>
          <h3>Longitude: </h3>
            <p className = 'answers'>{longitude}</p>  
          <h3>More Info:</h3>
            <p className = 'answers' style={{ wordBreak: 'break-word', overflowWrap: 'break-word' }}>
              <a href={url} target="_blank" rel="noreferrer">{url}</a>
            </p>   
          {/* <h3>Total Stored in Trie:</h3>
            <p className="answers">{trieCount}</p> */}
         </div>
      </div>     

      <div style={{ marginTop: '20px', marginRight: '220px' }}>

        <input
          type="text"
          placeholder="Location"
          value={location || ''}
          onChange={(e) => setLocation(e.target.value)}
          style={{
            padding: '8px',
            marginRight: '10px',
          }}
          />

        <button
          onClick={() => {
            if (location != null) {
              // Find earthquake matching entered location name
              const match = earthquakes.find((q) => q.location.toLowerCase() === location.toLowerCase()
              );
              if (match) {
                setLatitude(match.lat);
                setLongitude(match.long);
                setLocation(match.location);
                setMagnitude(match.magnitude);
                setURL(match.url);
                setMapCenter([match.lat, match.long]);
              } 
            }
          }}
          >
          </button>

        <input
          type="number"
          placeholder="Magnitude"
          value={magnitude !== null ? magnitude : ''}
          onChange={(e) => setMagnitude(e.target.value ? parseFloat(e.target.value) : null)}
          style={{
            padding: '8px',
            marginRight: '10px',
          }}
          />
        <button
          onClick={() => {
            if (magnitude != null) {
              // Find earthquake matching entered lat/lng
              const match = earthquakes.find((q) =>
                  Math.abs(q.magnitude - magnitude) < 0.01 
              );
              if (match) {
                setLatitude(match.lat);
                setLongitude(match.long);
                setLocation(match.location);
                setMagnitude(match.magnitude);
                setURL(match.url);
                setMapCenter([match.lat, match.long]);
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
