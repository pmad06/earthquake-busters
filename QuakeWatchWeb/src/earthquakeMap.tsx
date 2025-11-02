import React from 'react';
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
  return (
    <MapContainer
      center={[37.7749, -122.4194]} // default center
      zoom={5}
      style={{ height: '500px', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {earthquakes.map((quake, index) => (
        <Marker
          key={index}
          position={[quake.latitude, quake.longitude]}
        >
          <Popup>
            <strong>{quake.title}</strong>
            <br />
            Magnitude: {quake.magnitude}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};
