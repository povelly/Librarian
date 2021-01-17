import React, { Component } from "react";
import {Navbar} from "react-bootstrap";

export default class NavigationBar extends Component {

    render() {
        return (
            <Navbar bg="dark" variant="dark">
                <Navbar.Brand>Librarian</Navbar.Brand>
            </Navbar>
        );
    }
}