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

  useEffect(() => {
    fetch('http://127.0.0.1:5000/earthquakes')
      .then(res => res.json())
      .then(data => setEarthquakes(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>Earthquake Map</h1>
      <EarthquakeMap earthquakes={earthquakes} />
    </div>
  );
}
