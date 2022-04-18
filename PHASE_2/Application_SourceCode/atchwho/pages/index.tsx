import * as React from 'react';
import Head from 'next/head';
import Script from 'next/script';

import OurMap from '../components/ourmap';
import Overlay from '../components/Overlay';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';


export default function Home() {

	return (
		<html>
		<Head>
			<title>atchWHO</title>
		</Head>
		<Script src="https://unpkg.com/react/umd/react.production.min.js" />
		<Script src="https://unpkg.com/react-dom/umd/react-dom.production.min.js" />  
		<Script src="https://unpkg.com/react-bootstrap@next/dist/react-bootstrap.min.js" />
		<Script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" />
		<Script src="../styles/hehe.css" />
		<body style={{overflow: 'hidden', margin: 'auto'}}>
			<Overlay />
			<OurMap />
		</body>
		</html>
	);
}