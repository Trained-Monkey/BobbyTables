import * as React from 'react';
import { useState } from 'react';
import { ListGroup, InputGroup, FormControl, Button } from 'react-bootstrap';


export default function FlightQuerier() {
    const Amadeus = require('amadeus');
    
    const clientId = process.env.AMADEUS_CLIENT_ID;
    const clientSecret = process.env.AMADEUS_CLIENT_SECRET;

    const amadeus = new Amadeus({
        clientId: 'nrKMtUf0GuX3h7iawhqS4lOSgImGNnCM',
        clientSecret: 'rWueWloyP8J5JDSt',
        // clientId: clientId,
        // clientSecret: clientSecret,
    });

    const code: string = '';
    const [airport, setAirport] = useState(code);

    const flightResults: any[] = []
    const [resultsState, setResultsState] = useState(flightResults)

    // find all destinations served by a given airport
    function getDestinations(airportCode: string) {
        amadeus.shopping.flightDestinations.get({
            origin: airportCode,
        }).then((response: any) => {
            console.log(response.data);
            const data = response.data;
            const results: any[] = []
            for (const result of data) {
                const flight = {
                    origin: result.origin,
                    destination: result.destination,
                    price: result.price.total,
                    departureDate: result.departureDate,
                    returnDate: result.returnDate,
                }
                results.push(flight)
            }
            setResultsState(results)
            console.log(flightResults);
        }).catch((response: any) => {
            console.log(response);
        });
    }

    function handleAirportCodeChange(event: any) {
        setAirport(event.target.value);
    }

    // return a searchbar which allows the user to search for destinations based on the input
    // return a list of destinations based on the input
    return (
        <div>
            <InputGroup className="mb-3">
                <FormControl
                    placeholder="Departure Airport Code"
                    aria-label="Departure Airport Code"
                    aria-describedby="basic-addon2"
                    onChange={(event) => handleAirportCodeChange(event)}
                />
                <Button variant="outline-secondary" id="button-addon2" onClick={() => {getDestinations(airport)}}>
                    Search
                </Button>
            </InputGroup>
            <ListGroup as="div">
                {resultsState.map((result: any, index: number) => {
                    return (
                        <ListGroup.Item as="div" key={index}>
                            From {result.origin} To {result.destination} on {result.departureDate}<br />
                            From {result.destination} To {result.origin} on {result.returnDate}<br />
                            Price: ${result.price}
                        </ListGroup.Item>
                    )
                })}
            </ListGroup>
        </div>
    )

}