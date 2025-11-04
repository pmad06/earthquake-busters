import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
});

type Earthquake = {
  location: string;
  magnitude: number;
  lat: number;
  long: number;
  url: string;
};

interface Props {
  earthquakes: Earthquake[];
  center: [number, number];
  filterMagnitude?: number; // optional filter prop
}

export const EarthquakeMap: React.FC<Props> = ({ earthquakes, center, filterMagnitude }) => {
  // Filter earthquakes by magnitude if provided
  const displayedEarthquakes = filterMagnitude != null
    ? earthquakes.filter(q => Math.abs(q.magnitude - filterMagnitude) < 0.01)
    : earthquakes;

  return (
    <div>
      <MapContainer
        center={center}
        zoom={10}
        style={{ height: '500px', width: '100%' }}
        key={center.toString()}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {displayedEarthquakes.map((quake, index) => (
          <Marker key={index} position={[quake.lat, quake.long]}>
            <Popup>
              <strong>{quake.location}</strong>
              <br />
              Magnitude: {quake.magnitude}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};
