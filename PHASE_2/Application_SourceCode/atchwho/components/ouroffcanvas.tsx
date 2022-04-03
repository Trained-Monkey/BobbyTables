import React, { useEffect, useRef, useState } from "react";
import ReactDOM from "react-dom";
import { OffCanvas, OffCanvasMenu, OffCanvasBody } from "react-offcanvas";
import styled from "styled-components";


const offCanvas = ({ show , onHide} : { show:any , onHide:any}) => {
    const [isBrowser, setIsBrowser] = useState(false);
    const [isMenuOpened, setIsMenuOpened] = useState(false)

    useEffect(() => {
        setIsBrowser(true);
    }, []);

    const handleCloseClick = (event: MouseEvent) => {
        event.preventDefault();
        onHide();
    };

    const content = show ? (
        <OffCanvas width={300} transitionDuration={300} effect={"parallax"} isMenuOpened={isMenuOpened} position={"right"}>
            <OffCanvasBody className="bodyClass">
            <p>
                Click here to toggle the menu.
            </p>
            </OffCanvasBody>
            <OffCanvasMenu className="menuClass">
            <p>Placeholder content.</p>
            <ul>
                <li>Link 1</li>
                <li>Link 2</li>
                <li>Link 3</li>
                <li>Link 4</li>
                <li>Link 5</li>
                <li>
                <a href="#" onClick={handleCloseClick}>
                    Toggle Menu
                </a>
                </li>
            </ul>
            </OffCanvasMenu>
        </OffCanvas>
    ) : null;

    if (isBrowser) {
        return ReactDOM.createPortal(content, document.getElementById("offCanvas-root")!);
    } else {
        return null;
    }
};

const bodyClass = styled.div`
    background-color: #fff;
    padding: 100px;
`;
  
const menuClass = styled.div`
    background-color: #999;
    padding: 15px;
`;

export default offCanvas;