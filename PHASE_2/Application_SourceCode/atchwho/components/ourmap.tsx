import * as React from 'react';
import {Popup, Layer, Source, Marker, MapRef, Map} from 'react-map-gl';
import type {FillLayer} from 'react-map-gl';
import ArticleQuerier from './ArticleQuerier';
import FlightQuerier from './FlightQuerier';
import SubscriberQuerier from './SubscriberQuerier';

import Modal from './ourmodal';
import { useCallback } from 'react';
import { Button, Card, Offcanvas } from 'react-bootstrap';
import { Fab, Action } from 'react-tiny-fab';
import { TwitterTimelineEmbed, TwitterTweetEmbed} from 'react-twitter-embed';
import { useAppSelector, useAppDispatch } from '../app/hooks' 
import {clearArticles } from '../features/article/articleSlice'
import 'react-tiny-fab/dist/styles.css';

export default function OurMap() {

    const MAPBOX_TOKEN = 'pk.eyJ1IjoicG9pYm9pIiwiYSI6ImNsMTYwaTZuazAxOHMzaXFzdjkzZW4wNm8ifQ.MH9qcxmXZcPGKoMdz_eUvg'; // Set your mapbox token here
	const mapRef = React.useRef<MapRef>(null);
	const [vis, setVis] = React.useState(true);
	const [vis1, setVis1] = React.useState(true);
  
	const dispatch = useAppDispatch();

	const defaultSelCount: string[] = []
	const [selectedCountries, setSelectedCountries] = React.useState(defaultSelCount);
	const [showSide, setShowSide] = React.useState(false);
	const [showSide1, setShowSide1] = React.useState(false);
	const [showBottom, setShowBottom] = React.useState(false);
	const [showModal, setShowModal] = React.useState(false);
	const [showRoutes, setShowRoutes] = React.useState(false);
	const [showSubscriber, setShowSubscriber] = React.useState(false);

  	const handleCloseSide = () => setShowSide(false);
  	const handleShowSide = () => setShowSide(true);

	const handleCloseSide1 = () => setShowSide1(false);
  	const handleShowSide1 = () => setShowSide1(true);
	
	const handleCloseBottom = () => setShowBottom(false);
  	const handleShowBottom = () => setShowBottom(true);

	const handleCloseModal= () => setShowModal(false);
  	const handleShowModal = () => setShowModal(true);

	const handleCloseRoutes= () => setShowRoutes(false);
	const handleShowRoutes = () => setShowRoutes(true);
	
	const handleShowSubscriber = () => setShowSubscriber(true);
	const handleCloseSubscriber = () => setShowSubscriber(false);

	const asia = ['Sri Lanka', 'Kazakhstan', 'Tajikistan', 'Uzbekistan', 'Kyrgyzstan', 'Turkmenistan', 'Afghanistan', 'Pakistan', 'Azerbaijan', 'Armenia', 'Georgia', 'Turkey', 'Iraq', 'Iran', 'Syria', 'Jordan', 'Israel', 'Saudi Arabia', 'Oman', 'Yemen', 'Malaysia', 'Nepal', 'Bangladesh', 'India', 'Mongolia', 'South Korea', 'North Korea', 'Japan', 'China', 'Taiwan', 'Laos', 'Myanmar', 'Thailand', 'Cambodia', 'Vietnam', 'Philippines', 'Indonesia']
	const africa = ['Saint Helena, Ascension and Tristan da Cunha', 'Portugal', 'Spain', 'Cape Verde', 'Heard and McDonald Islands', 'French Southern and Antarctic Lands', 'Mayotte', 'Comoros', 'Mauritius', 'Reunion', 'Eswatini', 'Rwanda', 'Burundi', 'Malawi', 'Equatorial Guinea', 'Republic of the Congo', 'Gabon', 'Djibouti', 'Eritrea', 'Guinea-Bissau', 'Gambia', 'Benin', 'Togo', 'Ghana', 'Burkina Faso', 'Ivory Coast', 'Liberia', 'Sierra Leone', 'Guinea', 'Senegal', 'Mauritania', 'Mali', 'Morocco', 'Western Sahara', 'Egypt', 'Libya', 'Algeria', 'Niger', 'Nigeria', 'Cameroon', 'Chad', 'Central African Republic', 'Democratic Republic of the Congo', 'South Sudan', 'Sudan', 'Ethiopia', 'Somalia', 'Kenya', 'Uganda', 'Tanzania', 'Angola', 'Zambia', 'Zimbabwe', 'Mozambique', 'Lesotho', 'Botswana', 'Namibia', 'South Africa', 'Madagascar']
	const nAmerica = ['Turks and Caicos Islands', 'Bahamas', 'Trinidad and Tobago', 'Grenada', 'Barbados', 'Saint Vincent and the Grenadines', 'Saint Lucia', 'Martinique', 'Dominica', 'Guadeloupe', 'Virgin Islands', 'Puerto Rico', 'Jamaica', 'Haiti', 'Dominican Republic', 'Cuba', 'Honduras', 'El Salvador', 'Belize', 'Guatemala', 'Nicaragua', 'Panama', 'Costa Rica', 'Greenland', 'United States', 'Mexico', 'Canada']
	const sAmerica = ['French Guiana', 'Suriname', 'Guyana', 'Venezuela', 'Colombia', 'Peru', 'Ecuador', 'Bolivia', 'Paraguay', 'Brazil', 'Uruguay', 'South Georgia and South Sandwich Islands', 'Falkland Islands (Islas Malvinas)', 'Argentina', 'Chile']
	const europe = ['Montenegro', 'Serbia', 'Albania', 'Bosnia and Herzegovina', 'Croatia', 'Slovenia', 'Hungary', 'Slovakia', 'Czechia', 'Austria', 'Switzerland', 'Italy', 'France', 'Netherlands', 'Belgium', 'Denmark', 'Germany', 'Poland', 'Lithuania', 'Estonia', 'Latvia', 'Belarus', 'Ukraine', 'Moldova', 'Romania', 'North Macedonia', 'Kosovo', 'Bulgaria', 'Greece', 'Russia', 'Finland', 'Sweden', 'Norway', 'Iceland', 'Ireland', 'United Kingdom', 'Spain', 'Portugal']
	const oceania = ['US Minor Outlying Islands', 'Marshall Islands', 'Federated States of Micronesia', 'Kiribati', 'Tuvalu', 'Niue', 'Tonga', 'Fiji', 'Solomon Islands', 'Vanuatu', 'New Caledonia', 'Papua New Guinea', 'New Zealand', 'Australia']

	const articles = useAppSelector(state => state.articles.articles)
	//console.log(articles)
	
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

	const filter = React.useMemo(() => ["in", 'name_en', ...selectedCountries], [selectedCountries])

	const highlightLayer: FillLayer = {
		id: 'country_highlighted',
		type: 'fill',
		'source-layer': 'country_boundaries',
		filter: [
		  'all',
		  ['match', ['get', 'worldview'], ['all', 'US'], true, false],
		  ["!=", "true", ["get", "disputed"]],
		],
		paint: {
			'fill-color': 'rgba(255,130,0,1)',
		}
	}

	const countriesLayer: FillLayer = {
		id: 'country_boundaries',
		type: 'fill',
		'source-layer': 'country_boundaries',
		filter: [
		  'all',
		  ['match', ['get', 'worldview'], ['all', 'US'], true, false],
		  ["!=", "true", ["get", "disputed"]],
		],
		paint: {
		  'fill-outline-color': 'rgba(255,130,0,0.7)',
		  'fill-color': 'rgba(255,130,0,0.05)'
		}
	}
	
	function multiFunc(locations: any) {
		mapRef.current?.flyTo({center: [parseInt(locations[0].lng), parseInt(locations[0].lat)], zoom: 6})
		handleShowModal();
	}

    return (
		<div>
			<Map
				ref={mapRef}
				initialViewState={{
					latitude: 37.8,
					longitude: -122.4,
					zoom: 3
				}}
				style={{width: '100vw', height: '100vh', content: 'hidden', paddingTop: '10px'}}
				mapStyle="mapbox://styles/mapbox/dark-v10"
				mapboxAccessToken={MAPBOX_TOKEN}
				onClick={onclick}
                interactiveLayerIds={['country_boundaries']}				
			>	
				<button onClick={() => setVis(!vis)}>{vis ? "remove" : "add"}</button>
				<Fab alwaysShowTitle={true} icon="ℹ️">
					{vis && (
					<Action text="Search" onClick={showSide ? handleCloseSide : handleShowSide}>
						🔎
					</Action>
					)}
					{vis && (
					<Action text="Reports" onClick={showBottom ? handleCloseBottom : handleShowBottom}>
						📋
					</Action>
					)}
					{vis && (
					<Action text="Twitter" onClick={showSide1 ? handleCloseSide1 : handleShowSide1}>
						🕊️
					</Action>
					)}
					{vis && (
					<Action text="Clear" onClick={() => dispatch(clearArticles())}>
						🚫
          </Action>
          )}
          {vis && (
					<Action text="Manage Subscribers" onClick={showSubscriber ? handleCloseSubscriber : handleShowSubscriber}>
						❗
					</Action>
					)}
					{vis && (
					<Action text="Show Routes" onClick={showRoutes ? handleCloseRoutes : handleShowRoutes}>
						🛫
					</Action>
					)}
				</Fab>

				<button onClick={() => setVis1(!vis1)}>
					{vis1 ? "remove" : "add"}
				</button>
				<Fab style={{right: '105px', bottom: '24px'}} alwaysShowTitle={true} icon="🌎">
					{vis1 && (
					<Action text="Oceania" onClick={() => setSelectedCountries(oceania)}>
						📍
					</Action>
					)}
					{vis1 && (
					<Action text="Europe" onClick={() => setSelectedCountries(selectedCountries.concat(europe))}>
						📍
					</Action>
					)}
					{vis1 && (
					<Action text="S. America" onClick={() => setSelectedCountries(selectedCountries.concat(sAmerica))}>
						📍
					</Action>
					)}
					{vis1 && (
					<Action text="N. America" onClick={() => setSelectedCountries(selectedCountries.concat(nAmerica))}>
						📍
					</Action>
					)}
					{vis1 && (
					<Action text="Africa" onClick={() => setSelectedCountries(selectedCountries.concat(africa))}>
						📍
					</Action>
					)}
					{vis1 && (
					<Action text="Asia" onClick={() => setSelectedCountries(selectedCountries.concat(asia))}>
						📍
					</Action>
					)}
				</Fab>

                <Source type="vector" url="mapbox://mapbox.country-boundaries-v1">
                    <Layer beforeId="waterway-label" {...countriesLayer} />
					<Layer beforeId="waterway-label" {...highlightLayer} filter={filter}/>
				</Source>
				{
					articles.map((article, aIndex) => {
						return article.reports.map((report, rIndex) => {
							return report.locations.map((location, lIndex) => {
								return <Marker latitude={location.lat} longitude={location.lng} key={article.url + "-" + rIndex + "-" + lIndex}/>		
							})
						})
					})
				}
			</Map>

			<div id='offCanvas-root'>
				<Offcanvas show={showRoutes} onHide={handleCloseRoutes} scroll={true} backdrop={false} style={{width: 600}}>
					<Offcanvas.Header closeButton>
						<Offcanvas.Title>Search Recommanded Trips</Offcanvas.Title>
					</Offcanvas.Header>
					<Offcanvas.Body  style={{width: 600}}>
						<FlightQuerier />
						</Offcanvas.Body>
				</Offcanvas>
				
				<Offcanvas show={showSubscriber} onHide={handleCloseSubscriber} scroll={true} backdrop={false} style={{width: 600}}>
					<Offcanvas.Header closeButton>
					<Offcanvas.Title>Manage Notifications</Offcanvas.Title>
					</Offcanvas.Header>
					<Offcanvas.Body  style={{width: 600}}>
						<SubscriberQuerier countries={selectedCountries} setCountries={setSelectedCountries}/>
					</Offcanvas.Body>
				</Offcanvas>

				<Offcanvas show={showSide} onHide={handleCloseSide} scroll={true} backdrop={false} style={{width: 600}}>
					<Offcanvas.Header closeButton>
					<Offcanvas.Title>Search</Offcanvas.Title>
					</Offcanvas.Header>
					<Offcanvas.Body  style={{width: 600}}>
						<ArticleQuerier locations={selectedCountries}/>
					</Offcanvas.Body>
				</Offcanvas>

				<Offcanvas show={showSide1} onHide={handleCloseSide1} scroll={true} backdrop={false} style={{width: 600}}>
					<Offcanvas.Header closeButton>
					<Offcanvas.Title>Twitter</Offcanvas.Title>
					</Offcanvas.Header>
					<Offcanvas.Body  style={{width: 600}}>
						<TwitterTimelineEmbed
							sourceType="profile"
							screenName="CDCgov"
							options={{height: 800}}
							/>
					</Offcanvas.Body>
				</Offcanvas>

				<Offcanvas show={showBottom} onHide={handleCloseBottom} placement='bottom' scroll={true} backdrop={false} style={{height: 400}}>
					<Offcanvas.Header closeButton>
					<Offcanvas.Title>Reports</Offcanvas.Title>
					</Offcanvas.Header>
					<Offcanvas.Body  style={{width: '100%'}}>
					{
					articles.map((article, aIndex) => {
						return article.reports.map((report, rIndex) => {
							return <div style={{display: 'inline-grid'}} key={article.url + "-" + rIndex}>
								<Card style={{ width: '18rem', margin: '10px'}}>
									<Card.Body>
										<div style={{display: 'flex', justifyContent: 'flex-start'}}>
											<Card.Img variant='top' src="heart.png" style={{width: '30px', height: '30px', margin: '10px'}}/>
											<Card.Title>
												<a href={article.url}>{article.headline}</a>
											</Card.Title>
										</div>
										<Card.Text>
												Date: {article.date_of_publication}			
											<div>
												Diseases: {report.diseases.length == 0 ? "None" : report.diseases}
											</div>																			
												Syndromes: {report.syndromes.length == 0 ? "None" : report.syndromes}
										</Card.Text>
										<Button variant="btn btn-danger" onClick={(event) => multiFunc(report.locations)} value={article.headline}>Stay Updated</Button>
									</Card.Body>
								</Card>
							</div>
						})
					})
					}
					</Offcanvas.Body>
				</Offcanvas>
				
				<div id='modal-root'>
					<Modal show={showModal} onClose={handleCloseModal} title={"Subscribe to this marker"}>

					</Modal>
				</div>
			</div>
		</div>   
    )
}

