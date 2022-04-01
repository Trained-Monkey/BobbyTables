import * as React from 'react';
import Script from 'next/script';
import Map, {Popup, Layer, Source, Marker} from 'react-map-gl';
import {countriesLayer, highlightLayer} from '../pages/map-style';
import ArticleQuerier from './ArticleQuerier';
import { stringify } from 'querystring';
import { useCallback } from 'react';

import type {MapRef} from 'react-map-gl';
import { features } from 'process';

export default function OurMap() {

    const MAPBOX_TOKEN = 'pk.eyJ1IjoicG9pYm9pIiwiYSI6ImNsMTYwaTZuazAxOHMzaXFzdjkzZW4wNm8ifQ.MH9qcxmXZcPGKoMdz_eUvg'; // Set your mapbox token here

    const default_info = {longitude: -120, latitude: 40, countryName: "Australia"}
	
	//var default_info = null;
	const mapRef = React.useRef<MapRef>(null);
    const [hoverInfo, setHoverInfo] = React.useState(default_info);
	const [clickInfo, setClickInfo] = React.useState(default_info);

	function test() {
        var a = mapRef.current?.getStyle().layers
		console.log(a)
    }
    
	const onclick = useCallback(event => {
		const {
			features,
		} = event;

		var country = (event.features && event.features[0]).properties['name_en']

	}, []);

    const onHover = useCallback(event => {
		
		const {
			features,
		} = event;

        const country = event.features && event.features[0];

		var new_state = {
			longitude: event.lngLat.lng, 
			latitude: event.lngLat.lat, 
			countryName: country.properties['name_en']
		}

        setHoverInfo(new_state);
    }, []);

	const selectedCountry = (hoverInfo.hasOwnProperty('countryName')) ? hoverInfo && hoverInfo.countryName : '';
	const filter = React.useMemo(() => ['in', 'color_group', selectedCountry], [selectedCountry]);

    return (
		<div>
			<ArticleQuerier />
			<button onClick={test}>Click me</button>
			<Map
				ref={mapRef}
				initialViewState={{
					latitude: 37.8,
					longitude: -122.4,
					zoom: 3
				}}
				style={{width: '100vw', height: '100vh', content: 'hidden'}}
				mapStyle="mapbox://styles/mapbox/dark-v10"
				mapboxAccessToken={MAPBOX_TOKEN}
                onMouseMove={onHover}
				onClick={onclick}
                interactiveLayerIds={['country_boundaries']}
				
			>
                <Source type="vector" url="mapbox://mapbox.country-boundaries-v1">
                    <Layer beforeId="waterway-label" {...countriesLayer} />
					<Layer beforeId="waterway-label" {...highlightLayer} filter={filter} />
				</Source>
                
				{selectedCountry && (
					<Popup
						longitude={hoverInfo.longitude}
						latitude={hoverInfo.latitude}
						offset={[0, -10]}
						closeButton={false}
						className="county-info"
					>
						{selectedCountry}
					</Popup>
				)}
			</Map>
		</div>
        
    )
}