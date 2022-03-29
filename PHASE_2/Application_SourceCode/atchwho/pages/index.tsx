import * as React from 'react';
import Head from 'next/head';
import Map, {Marker} from 'react-map-gl';

import OurMap from '../components/ourmap';

import 'mapbox-gl/dist/mapbox-gl.css';


export default function Home() {


  return (
    <>
      <Head>
        <title>atchWHO</title>
      </Head>
      <body style={{overflow: 'hidden', margin: 'auto'}}>
        <OurMap />
      </body>
    </>
  );
}