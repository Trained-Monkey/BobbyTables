import React, { useEffect, useRef, useState } from "react";
import ReactDOM from "react-dom";
import { Button } from 'react-bootstrap';
import styled from "styled-components";


const Modal = ({ show , onClose, children, title } : { show:any , onClose:any, children:any, title:any }) => {
    const [isBrowser, setIsBrowser] = useState(false);
  
    useEffect(() => {
      setIsBrowser(true);
    }, []);
  
    const handleCloseClick = (event: React.MouseEvent) => {
      event.preventDefault();
      onClose();
    };
  
    const modalContent = show ? (
      <StyledModalOverlay>
        <StyledModal>
          <StyledModalHeader>
            <div>
              {title}
            </div>
            <div style={{right: '0px'}}>
              <a href="#" onClick={handleCloseClick}>
                x
              </a>
            </div>
          </StyledModalHeader>
          <StyledModalBody>
            <Button variant="btn btn-primary w-50 rounded-pill b1">
              Subscribe
            </Button>
          </StyledModalBody>
        </StyledModal>
      </StyledModalOverlay>
    ) : null;
  
    if (isBrowser) {
      return ReactDOM.createPortal(modalContent, document.getElementById("modal-root")!);
    } else {
      return null;
    }
};
  
const StyledModalBody = styled.div`
    padding: 1em;
    border-radius: 25px;
    display: flex;
    justify-content: center;
`;

const StyledModalTitle = styled.div`
    font-size: 25px;
`;

const StyledModalHeader = styled.div`
    display: flex;
    justify-content: space-around;
    width: 120%;
    font-size: 25px;
`;

const StyledModal = styled.div`
    display: grid;
    justify-content: center;
    border: 2px solid rgba(255,130,0,1); 
    background: rgba(255,255,255,0.7);
    width: 30%;
    height: 20%;
    border-radius: 5px;
    padding: 5px;
`;

const StyledModalOverlay = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 600px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
    padding: 1em;
`;
  
export default Modal;