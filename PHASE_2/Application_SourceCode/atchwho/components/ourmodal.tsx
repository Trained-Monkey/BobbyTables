import React, { useEffect, useRef, useState } from "react";
import ReactDOM from "react-dom";
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
            <a href="#" onClick={handleCloseClick}>
              x
            </a>
          </StyledModalHeader>
          {title && <StyledModalTitle>{title}</StyledModalTitle>}
          <StyledModalBody>{children}</StyledModalBody>
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
`;

const StyledModalTitle = styled.div`
    font-size: 25px;
`;

const StyledModalHeader = styled.div`
    display: flex;
    justify-content: flex-end;
    font-size: 25px;
`;

const StyledModal = styled.div`
    display: grid;
    justify-content: center;
    background: #c2c2c2;
    width: 650px;
    height: 600px;
    border-radius: 5px;
    padding: 5px;
`;

const StyledModalOverlay = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
    padding: 1em;
`;
  
export default Modal;