import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

// Fix default marker icon issue in Leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl, 
  iconUrl,
  shadowUrl,
});

type Earthquake = {
  title: string;
  magnitude: number;
  latitude: number;
  longitude: number;
};

interface Props {
  earthquakes: Earthquake[];
}

export const EarthquakeMap: React.FC<Props> = ({ earthquakes }) => {
  const [searchTerm, setSearchTerm] = useState('');

  // Filter earthquakes based on search term (case-insensitive)
  const filteredQuakes = earthquakes.filter(q =>
    q.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      {/*Search Bar */}
      <div style={{ marginBottom: '10px', textAlign: 'center' }}>
        <input
          type="text"
          placeholder="Search earthquakes..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            padding: '8px',
            width: '80%',
            maxWidth: '400px',
            borderRadius: '4px',
            border: '1px solid #ccc'
          }}
        />
      </div>

      {/* Map */}
      <MapContainer
        center={[37.7749, -122.4194]}
        zoom={5}
        style={{ height: '500px', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {filteredQuakes.map((quake, index) => (
          <Marker key={index} position={[quake.latitude, quake.longitude]}>
            <Popup>
              <strong>{quake.title}</strong>
              <br />
              Magnitude: {quake.magnitude}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};
