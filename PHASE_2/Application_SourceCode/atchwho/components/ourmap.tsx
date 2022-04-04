import * as React from 'react';
import Script from 'next/script';
import Map, {Popup, Layer, Source, Marker} from 'react-map-gl';
import {countriesLayer, highlightLayer} from '../pages/map-style';
import ArticleQuerier from './ArticleQuerier';
import Modal from './ourmodal';
import { stringify } from 'querystring';
import { useCallback } from 'react';
import { OffCanvas } from 'react-offcanvas';
import { Button } from 'react-bootstrap';
import { Card } from 'react-bootstrap';
import { Offcanvas } from 'react-bootstrap';
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

	const [showCanvas, setShowCanvas] = React.useState(false);
	const [showSide, setShowSide] = React.useState(false);
	const [showBottom, setShowBottom] = React.useState(false);

  	const handleCloseSide = () => setShowSide(false);
  	const handleShowSide = () => setShowSide(true);
	
	const handleCloseBottom = () => setShowBottom(false);
  	const handleShowBottom = () => setShowBottom(true);

	const articles = useAppSelector(state => state.articles.articles)
	console.log(articles)

	function test() {
        var a = mapRef.current?.getStyle().layers
		console.log(a)
    }
	
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

    return (
		<div>
			<Button variant="primary" onClick={handleShowSide}>SIDE</ Button>
			<Button variant="primary" onClick={handleShowBottom}>BOTTOM</ Button>
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

			<div id='offCanvas-root'>
				<Offcanvas show={showSide} onHide={handleCloseSide} style={{width: 600}}>
					<Offcanvas.Header closeButton>
					<Offcanvas.Title>Offcanvas</Offcanvas.Title>
					</Offcanvas.Header>
					<Offcanvas.Body  style={{width: 600}}>
						<ArticleQuerier locations={selectedCountries}/>
					</Offcanvas.Body>
				</Offcanvas>

				<Offcanvas show={showBottom} onHide={handleCloseBottom} placement='bottom' style={{height: 400}}>
					<Offcanvas.Header closeButton>
					<Offcanvas.Title>Reports</Offcanvas.Title>
					</Offcanvas.Header>
					<Offcanvas.Body  style={{width: '100%'}}>
					{
					articles.map((article, aIndex) => {
						return article.reports.map((report, rIndex) => {
							return <div style={{display: 'inline-grid'}} key={article.url + "-" + rIndex}>
								<Card style={{ width: '18rem', margin: '10px'}}>
									<Card.Img variant='top' src="heart.png" style={{width: '50px', height: '50px', margin: '5px'}}/>
									<Card.Body>
										<Card.Title>{article.headline}</Card.Title>
										<Card.Text>
											<div>
												{article.date_of_publication}
											</div>												
											<a href={article.url}>Link</a>
										</Card.Text>
										<Button variant="primary">Button</Button>
									</Card.Body>
								</Card>
							</div>
						})
					})
					}
					</Offcanvas.Body>
				</Offcanvas>
			</div>
		</div>   
    )
}