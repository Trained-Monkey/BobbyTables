import * as React from 'react';
import Script from 'next/script';
import Map, {Popup, Layer, Source, Marker} from 'react-map-gl';
import {countriesLayer, highlightLayer} from '../pages/map-style';
import ArticleQuerier from './ArticleQuerier';
import Modal from './ourmodal';
import { stringify } from 'querystring';
import { useCallback } from 'react';

import { useAppSelector, useAppDispatch } from '../app/hooks' 

import type {MapRef} from 'react-map-gl';
import { features } from 'process';

export default function OurMap() {

    const MAPBOX_TOKEN = 'pk.eyJ1IjoicG9pYm9pIiwiYSI6ImNsMTYwaTZuazAxOHMzaXFzdjkzZW4wNm8ifQ.MH9qcxmXZcPGKoMdz_eUvg'; // Set your mapbox token here

    const default_info = {longitude: -120, latitude: 40, countryName: "Australia"}
	
	//var default_info = null;
	const mapRef = React.useRef<MapRef>(null);
	const [clickInfo, setClickInfo] = React.useState(default_info);
  
	const defaultSelCount: string[] = []
	const [selectedCountries, setSelectedCountries] = React.useState(defaultSelCount);

	const [showModal, setShowModal] = React.useState(false);

	const articles = useAppSelector(state => state.articles.articles)
	console.log(articles)

	function test() {
        var a = mapRef.current?.getStyle().layers
		console.log(a)
    }

	  /*
	const onclick = useCallback(event => {
		const {
			features,
		} = event;

		var country = (event.features && event.features[0]).properties['name_en']
		mapRef.current?.flyTo({center: [parseInt(event.lngLat.lng), parseInt(event.lngLat.lat)], zoom: 4})
		// pass country to query string
		// receive articles
		// get reports from articles
		let articles= myJSON.articles
		let articles_len = articles.length
		for (let i = 0; i < articles_len; i++) {
			let reports = myJSON.articles[i].article.reports
			let reports_len = reports.length
			for (let j = 0; j < reports_len; j++) {
				let report_locations = reports[j].locations
				let report_locations_len = report_locations.length
				for (let k = 0; k < report_locations_len; k++) {
					
					//console.log(report_locations[k].country)
					//console.log(report_locations[k].location)
				}
			}
		}
		// place marker on location from report
		// place report info in bootstrap card

	}, []);
	*/
	
	const onclick = useCallback(event => {
		const {
			features,
		} = event;

		var country = (event.features && event.features[0]).properties['name_en']
		console.log(country)
		if (selectedCountries.includes(country)) {
			const newCountries: string[] = []
			selectedCountries.forEach((selCountry) => {
				if (selCountry !== country) {
					newCountries.push(selCountry)
				}
			})
			setSelectedCountries(newCountries)
		} else {
			const newCountries: string[] = [country]
			setSelectedCountries(newCountries.concat(selectedCountries))
		}
	}, [selectedCountries]);

	function fetchData(location: string) {
		//if (articleQuerierRef.current) {
		//	articleQuerierRef.current.doFetch(location)
		//}
	}

	const filter = React.useMemo(() => ["in", 'name_en', ...selectedCountries], [selectedCountries])

    return (
		<div>
			<button onClick={() => setShowModal(true)}>Open Modal</button>
			<button onClick={() => fetchData('Malawi')}>Click me</button>
			<Map
				ref={mapRef}
				initialViewState={{
					latitude: 37.8,
					longitude: -122.4,
					zoom: 3
				}}
				style={{width: '100vw', height: '90vh', content: 'hidden', paddingTop: '10px'}}
				mapStyle="mapbox://styles/mapbox/dark-v10"
				mapboxAccessToken={MAPBOX_TOKEN}
				onClick={onclick}
                interactiveLayerIds={['country_boundaries']}				
			>
                <Source type="vector" url="mapbox://mapbox.country-boundaries-v1">
                    <Layer beforeId="waterway-label" {...countriesLayer} />
					<Layer beforeId="waterway-label" {...highlightLayer} filter={filter}/>
				</Source>
				{
					articles.map((article, aIndex) => {
						return article.reports.map((report, rIndex) => {
							return report.locations.map((location, lIndex) => {
								console.log(location)
								return <Marker latitude={location.lat} longitude={location.lng} key={article.url + "-" + rIndex + "-" + lIndex}/>
							})
						})
					})
				}
			</Map>

			<div id='modal-root'>
				<Modal onClose={() => setShowModal(false)} show={showModal} title={"Date Selection"}>
					<ArticleQuerier locations={selectedCountries}/>
				</Modal>
			</div>
		</div>
        
    )
}