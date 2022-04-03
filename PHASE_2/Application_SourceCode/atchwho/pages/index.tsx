import * as React from 'react';
import Head from 'next/head';
import Script from 'next/script';
import Map, {Marker} from 'react-map-gl';


import OurMap from '../components/ourmap';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';


export default function Home() {

	return (
		<html>
		<Head>
			<title>atchWHO</title>
			<Script src="https://unpkg.com/react/umd/react.production.min.js" />
			<Script src="https://unpkg.com/react-dom/umd/react-dom.production.min.js" />  
			<Script src="https://unpkg.com/react-bootstrap@next/dist/react-bootstrap.min.js" />
		</Head>
		<body style={{overflow: 'hidden', margin: 'auto'}}>
			<OurMap />
		</body>
		</html>
	);
}