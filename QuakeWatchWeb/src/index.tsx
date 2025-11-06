import React, { useEffect, useState } from 'react';
import { EarthquakeMap } from './earthquakeMap';
import 'leaflet/dist/leaflet.css';

type Earthquake = {
  location: string;
  magnitude: number;
  lat: number;
  long: number;
  url: string;
  risk_factor: string; 
};

export default function Home() {
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);
  const [suggestions, setSuggestions] = useState<Earthquake[]>([]); //addition for my trie - not in splay rn

  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);
  const [magnitude, setMagnitude] = useState<number | null>(null);
  const [location, setLocation] = useState('');
  const [url, setURL] = useState('');
  const [mapCenter, setMapCenter] = useState<[number, number]>([37.7749, -122.4194]);
  const [riskFactor, setRiskFactor] = useState('');
 
  useEffect(() => {
    fetch('http://127.0.0.1:5000/earthquakes')
      .then(res => res.json())
      .then(data => setEarthquakes(data))
      .catch(err => console.error(err));
  }, []);

  //debounce
  useEffect(() => {
    const delay = setTimeout(() => {
      if (location.length > 1) {
        fetch(`http://127.0.0.1:5000/search_trie/${encodeURIComponent(location)}`)
          .then(res => res.json())
          //.then(data => setSuggestions(data))
          .then(data => {
            console.log("Autocomplete results:", data);
            setSuggestions(data);
            setEarthquakes(data);
          })
          .catch(err => console.error(err));
      } else {
        setSuggestions([]);
      }
    }, 300);
  
  
    return () => clearTimeout(delay);
  }, [location]);
  
  const handleMagnitudeSearch = () => {
    if (magnitude == null) return;
  
    fetch(`http://127.0.0.1:5000/earthquakes/search/${magnitude}`)
      .then(res => res.json())
      .then((data: Earthquake[]) => {
        if (data.length > 0) {
         
          const firstMatch = data[0];
          setLatitude(firstMatch.lat);
          setLongitude(firstMatch.long);
          setLocation(firstMatch.location);
          setMagnitude(firstMatch.magnitude);
          setURL(firstMatch.url);
          setRiskFactor(firstMatch.risk_factor);
  
          setMapCenter([firstMatch.lat, firstMatch.long]);
  
          setEarthquakes(data);
        } else {
          alert("No earthquakes found with that magnitude");
        }
      })
      .catch(err => console.error(err));
  };

  return (
    <>
      <header>
        Earthquake Risk Guide
      </header>
      <div id = "homepage">
        <h1>Earthquake Map</h1>
        <div style={{ display: 'flex', gap: '20px', marginTop: '20px', width: '100%', maxWidth: '1200px' }}>
          <div style={{ flex: 3 }}>
            <EarthquakeMap earthquakes={earthquakes} center={mapCenter} />
          </div>
          <div id = "sidebar" style ={{ flex: 1}}>
            <h3>Location: </h3>
              <p className = 'answers'>{location}</p>
            <h3>Latitude, Longitude: </h3>
              <p className = 'answers'>{latitude} {longitude}</p> 
            <h3>More Info:</h3>
              <p className = 'answers' style={{ wordBreak: 'break-word', overflowWrap: 'break-word' }}>
                <a href={url} target="_blank" rel="noreferrer">{url}</a>
              </p>   
          
            {/* <h3>Total Stored in Trie:</h3>
              <p className="answers">{trieCount}</p> */}
          </div>
        </div>     

        <div style={{ marginTop: '20px', marginRight: '320px' }}>
          <div style={{ position: "relative", display: "inline-block" }}>
            <input
              type="text"
              placeholder="Location (City, State)"
              value={location || ''}
              onChange={(e) => setLocation(e.target.value)}
              style={{
                padding: '8px',
                marginRight: '10px',
              }}
              />
              {suggestions.length > 0 && (
                <ul style={{
                  position: "absolute",
                  top: "100%",
                  left: 0,
                  right: 0,
                  background: "#fff",
                  border: "1px solid #ccc",
                  maxHeight: "150px",
                  overflowY: "auto",
                  zIndex: 1000,
                  margin: 0,
                  padding: 0,
                  listStyle: "none"
                }}>
                  {suggestions.map((s, idx) => (
                    <li
                      key={idx}
                      style={{
                        padding: "4px",
                        cursor: "pointer",
                        backgroundColor: "white",
                        color: "black"
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.background = "#eee"}
                      onMouseLeave={(e) => e.currentTarget.style.background = "white"}
                      // onClick={() => {
                      //   setLocation(s.location);
                      //   setLatitude(s.lat);
                      //   setLongitude(s.long);
                      //   setMagnitude(s.magnitude);
                      //   setURL(s.url);
                      //   setMapCenter([s.lat, s.long]);
                      //   setSuggestions([]);
                      // }}
                      onClick={() => {
                        setLocation(s.location);
                        setLatitude(s.lat);
                        setLongitude(s.long);
                        setMagnitude(s.magnitude);
                        setURL(s.url);
                        setMapCenter([s.lat, s.long]);
                        setSuggestions([]);
                        setRiskFactor(s.risk_factor);
                      }}

                    >
                      {s.location}
                    </li>
                  ))}
                </ul>
              )}
          </div>
            <button
            onClick={() => {
              if (location && earthquakes.length > 0) {
                const match = earthquakes.find(
                  (q) => q.location.toLowerCase() === location.toLowerCase()
                );
                if (match) {
                  setLatitude(match.lat);
                  setLongitude(match.long);
                  setLocation(match.location);
                  setMagnitude(match.magnitude);
                  setURL(match.url);
                  setMapCenter([match.lat, match.long]);
                  setRiskFactor(match.risk_factor);
                }
              }
            }}
          >
            Move Map
          </button>
            <input
              type="number"
              placeholder="Magnitude"
              value={magnitude !== null ? magnitude : ''}
              onChange={(e) => setMagnitude(e.target.value ? parseFloat(e.target.value) : null)}
              style={{ padding: '8px', marginRight: '10px' }}
            />
            <button onClick={handleMagnitudeSearch}>Move Map</button>
          </div> 
      </div>
    </>  
  );
}
