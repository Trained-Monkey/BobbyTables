import * as React from 'react';
import { useState, forwardRef } from 'react';

const axios = require('axios')



export default function SubscriberQuerier({ countries, setCountries }) {
    const [email, setEmail] = React.useState("");
    const [content, setContent] = React.useState("");
    const [addVis, setAddVis] = React.useState(false);
    const [updVis, setUpdVis] = React.useState(false);
    const [remVis, setRemVis] = React.useState(false);

    function hideAll(){
        setUpdVis(false);
        setRemVis(false);
        setAddVis(false);
    }

    function changeEmail(email: string) {
        hideAll();
        setEmail(email);
        setContent("");
    }

    function sendEmail(email: string) {
        const params = {
            email: email
        }

        axios.get("http://127.0.0.1:8000/subscriber", { params })
            .then((response: any) => {
                setCountries(response.data.locations);
                hideAll();
                setRemVis(true);
                setUpdVis(true);
                // Unsubscribed 
                setContent("Subscriber found, showing subscribed locations")
                // Update
            })
            .catch((response: any) => {
                hideAll();
                setAddVis(true);
                
                setContent("No subscriber found with that email, please select locations and subscribe")
            })
    }

    function updateSubscriber(email: string) {
        const params = {
            email: email,
            location: countries.join(',')
        }

        axios.patch("http://127.0.0.1:8000/subscriber", null, { params })
            .then((response: any) => {
                setContent("Subscriber has been updated")
            })
            .catch((response: any) => {
                setContent("No subscriber with that email exists")
            })

    }

    function removeSubscriber(email: string) {
        const params = {
            email: email
        }

        axios.delete("http://127.0.0.1:8000/subscriber", { params })
            .then((response: any) => {
                setContent("Subscriber has been removed")
                hideAll();
                setAddVis(true);
            })
            .catch((response: any) => {
                setContent("No subscriber with that email exists")
            })
    }

    function addSubscriber(email: string) {

        const params = {
            email: email,
            location: countries.join(',')
        }

        axios.put("http://127.0.0.1:8000/subscriber", null, { params })
            .then((response: any) => {
                hideAll();
                setRemVis(true);
                setUpdVis(true);
                setContent("Subscriber has been added")
            })
            .catch((response: any) => {
                setContent("Subscriber with that email already exists! Click send to show subscribed locations")
            })
    }


    return (
        <div>
            <div style={{ maxWidth: 575 }}>
                <label >
                    Email:
                    <input style={{margin: "5px"}} type="text" name="email" value={email} onChange={evt => changeEmail(evt.target.value)} />
                </label>
                <button onClick={() => sendEmail(email)}>
                    Set
                </button>

                <div style={{display: "flex", justifyContent: "space-between", width: "50%", margin: "5px"}}>
                    {addVis && (
                        <button style={{display: "table-cell", textAlign:"center"}} onClick={() => addSubscriber(email)}>
                        Subscribe
                        </button>
					)}
                    
                    {remVis && (
                        <button style={{display: "table-cell", textAlign:"center"}} onClick={() => removeSubscriber(email)}>
                            Unsubscribe
                        </button>
                    )}

                    {updVis && (
                        <button style={{display: "table-cell", textAlign:"center"}} onClick={() => updateSubscriber(email)}>
                            Update
                        </button>
                    )}
                </div>

            </div>
            <p>
                {content}
            </p>

        </div>


    )
}