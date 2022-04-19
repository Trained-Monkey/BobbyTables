import React, {useState} from "react";
import { Button } from 'react-bootstrap';
import Carousel from 'react-bootstrap/Carousel'
import styled from "styled-components";
import Modal from 'react-bootstrap/Modal';

const Overlay = () => {
    const [show, setShow] = useState(true);
    const [page, setPage] = useState(0);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const what = ("AchWHO is your favourite source for accurate, up-to-date information about ongoing pandemics and outbreaks around the world. Data from the World Health Organisation combined with an interactive map simplifies the process of examining specific countries and planning appropriate safety measures.")
    /* const how = [
        "EXPLORE:",
        "ANALYSE:",
        "MONITOR:"
    ] */

    const Modal1 = (
        <Modal.Body>
            <h5>What is achWHO?</h5>
            <p>{what}</p>
            <h5>How to use achWHO:</h5>
            <ul>
                <li>
                    EXPLORE: Wander around the map and select your countries of interest. 
                </li>
                <li>
                    ANALYSE: Use filters to locate the information you need and observe important reports regarding areas of concern. 
                </li>
                <li>
                    OBSERVE: Browse relevant Twitter feeds directly from the app. 
                </li>
                <li>
                    MONITOR: Subscribe to push notification updates to continue to stay up-to-date and thus effectively plan safe travel routes. 
                </li>
            </ul>
        </Modal.Body>
    );

    return(
        <>
            {/* <p>hi</p>
            <Button variant="primary" onClick={handleShow}>
            Launch demo modal
            </Button> */}
    
            <Modal 
                show={show} 
                onHide={handleClose} 
                size="lg" 
                centered
            >
            <Modal.Header closeButton >
                <Modal.Title>Welcome to achWHO</Modal.Title>
            </Modal.Header>
            <LandingModal>
                {page == 0 && Modal1}
            </LandingModal>

            <Modal.Footer>
                <Button variant="primary" onClick={handleClose}>
                    Go!
                </Button>
            </Modal.Footer>
            </Modal>
        </>

    );
}


export default Overlay;

const LandingModal = styled.div`
    height: 50vh;
`;

const LandingModalFooter = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

const CentredDiv = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

const FooterMenu = styled.div`
    display: flex;
    flex-direction: row;
`