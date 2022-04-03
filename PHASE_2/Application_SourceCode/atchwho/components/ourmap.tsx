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
	const [clickInfo, setClickInfo] = React.useState(default_info);
	const defaultSelCount: string[] = []
	const [selectedCountries, setSelectedCountries] = React.useState(defaultSelCount);

	var locations: string;

	function test() {
        var a = mapRef.current?.getStyle().layers
		console.log(a)
    }
    
	var myJSON = {
		"articles": [
		  {
			"article": {
			  "url": "https://www.who.int/csr/don/17-january-2020-novel-coronavirus-japan-ex-china/en/",
			  "date_of_publication": "A very nice Item",
			  "headline": "Novel Coronavirus – Japan (ex-China)",
			  "main_text": "On 15 January 2020, the Ministry of Health, Labour and Welfare, Japan (MHLW) reported an imported case of laboratory-confirmed 2019-novel coronavirus (2019-nCoV) from Wuhan, Hubei Province, China. The case-patient is male, between the age of 30-39 years, living in Japan. The case-patient travelled to Wuhan, China in late December and developed fever on 3 January 2020 while staying in Wuhan. He did not visit the Huanan Seafood Wholesale Market or any other live animal markets in Wuhan. He has indicated that he was in close contact with a person with pneumonia. On 6 January, he traveled back to Japan and tested negative for influenza when he visited a local clinic on the same day.",
			  "reports": [
				{
				  "event_date": "2020-01-03 xx:xx:xx to 2020-01-15",
				  "locations": [
					{
					  "country": "China",
					  "location": "Wuhan, Hubei Province"
					},
					{
					  "country": "Japan",
					  "location": ""
					}
				  ],
				  "diseases": [
					"2019-nCoV"
				  ],
				  "syndromes": [
					"Fever of unknown Origin"
				  ]
				}
			  ]
			},
			"articleId": 0
		  }
		],
		"max_articles": 0
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

	const articleQuerierRef = React.useRef();

	function fetchData(location: string) {
		//if (articleQuerierRef.current) {
		//	articleQuerierRef.current.doFetch(location)
		//}
	}

	const filter = React.useMemo(() => ["in", 'name_en', ...selectedCountries], [selectedCountries])

    return (
		<div>
			<ArticleQuerier ref = {articleQuerierRef} locations={selectedCountries} />
			<button onClick={fetchData('Malawi')}>Click me</button>
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
				onClick={onclick}
                interactiveLayerIds={['country_boundaries']}				
			>
                <Source type="vector" url="mapbox://mapbox.country-boundaries-v1">
                    <Layer beforeId="waterway-label" {...countriesLayer} />
					<Layer beforeId="waterway-label" {...highlightLayer} filter={filter}/>
				</Source>    
			</Map>
		</div>
        
    )
}