import * as React from 'react';
import Head from 'next/head';
import Map, {Marker} from 'react-map-gl';

import 'mapbox-gl/dist/mapbox-gl.css';

const MAPBOX_TOKEN = 'pk.eyJ1IjoicG9pYm9pIiwiYSI6ImNsMTYwaTZuazAxOHMzaXFzdjkzZW4wNm8ifQ.MH9qcxmXZcPGKoMdz_eUvg'; // Set your mapbox token here

export default function Home() {
  return (
    <div>
      <Head>
        <title>atchWHO</title>
      </Head>
      <body style={{overflow: 'hidden', margin: 'auto'}}>
        <Map
          initialViewState={{
            latitude: 37.8,
            longitude: -122.4,
            zoom: 14
          }}
          style={{width: '100vw', height: '100vh', content: 'hidden'}}
          mapStyle="mapbox://styles/mapbox/dark-v10"
          mapboxAccessToken={MAPBOX_TOKEN}
        >
          <Marker longitude={-122.4} latitude={37.8} color="red" />
        </Map>
      </body>
    </div>
  );
}