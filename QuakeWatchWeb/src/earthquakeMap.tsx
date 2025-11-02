import React, { useState } from 'react';
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
}

export const EarthquakeMap: React.FC<Props> = ({ earthquakes, center }) => {
  return (
    <div>
      {/* Map */}
      <MapContainer
        center={center}
        zoom={5}
        style={{ height: '500px', width: '100%' }}
        key = {center.toString()}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {earthquakes.map((quake, index) => (
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



