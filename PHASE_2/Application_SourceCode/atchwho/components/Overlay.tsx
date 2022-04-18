import React, {useState} from "react";
import { Button } from 'react-bootstrap';
import styled from "styled-components";
import Modal from 'react-bootstrap/Modal'

const Overlay = () => {
    const [show, setShow] = useState(true);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

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
            <Modal.Header closeButton>
                <Modal.Title>Welcome to achWHO</Modal.Title>
            </Modal.Header>
            <LandingModal>

                <Modal.Body>
                    <h5>What is achWHO?</h5>
                    <p>hdfhidhf</p>
                    <h5>How to use achWHO:</h5>
                    <p>hdfhidhf</p>
                </Modal.Body>

            </LandingModal>
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