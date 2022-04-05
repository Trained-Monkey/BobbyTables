import * as React from 'react';
import Script from 'next/script';
import {Popup, Layer, Source, Marker, MapRef, Map} from 'react-map-gl';
import type {FillLayer} from 'react-map-gl';
import ArticleQuerier from './ArticleQuerier';
import Modal from './ourmodal';
import { stringify } from 'querystring';
import { useCallback } from 'react';
import { Button, Card, Offcanvas } from 'react-bootstrap';
import { Fab, Action } from 'react-tiny-fab';
import { useAppSelector, useAppDispatch } from '../app/hooks' 
import 'react-tiny-fab/dist/styles.css';
import { features } from 'process';

export default function OurMap() {

    const MAPBOX_TOKEN = 'pk.eyJ1IjoicG9pYm9pIiwiYSI6ImNsMTYwaTZuazAxOHMzaXFzdjkzZW4wNm8ifQ.MH9qcxmXZcPGKoMdz_eUvg'; // Set your mapbox token here
	//var default_info = null;
	const mapRef = React.useRef<MapRef>(null);
	const [vis, setVis] = React.useState(true);
  
	const defaultSelCount: string[] = []
	const [selectedCountries, setSelectedCountries] = React.useState(defaultSelCount);

	const [showCanvas, setShowCanvas] = React.useState(false);
	const [showSide, setShowSide] = React.useState(false);
	const [showBottom, setShowBottom] = React.useState(false);
	const [showModal, setShowModal] = React.useState(false);

  	const handleCloseSide = () => setShowSide(false);
  	const handleShowSide = () => setShowSide(true);
	
	const handleCloseBottom = () => setShowBottom(false);
  	const handleShowBottom = () => setShowBottom(true);

	const handleCloseModal= () => setShowModal(false);
  	const handleShowModal = () => setShowModal(true);

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
					<Action text="Search" onClick={showSide ? handleCloseSide : handleShowSide}>
						🔎
					</Action>
					{vis && (
					<Action text="Reports" onClick={showBottom ? handleCloseBottom : handleShowBottom}>
						📋
					</Action>
					)}
					<Action text="Clear Countries" onClick={() => setSelectedCountries([])}>
						🚫
					</Action>
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
				<Offcanvas show={showSide} onHide={handleCloseSide} scroll={true} backdrop={false} style={{width: 600}}>
					<Offcanvas.Header closeButton>
					<Offcanvas.Title>Offcanvas</Offcanvas.Title>
					</Offcanvas.Header>
					<Offcanvas.Body  style={{width: 600}}>
						<ArticleQuerier locations={selectedCountries}/>
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

