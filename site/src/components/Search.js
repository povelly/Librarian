import React, { Component } from "react";
import { Button, Form, Alert } from "react-bootstrap";

import "../style/search.css"

export default class Search extends Component {

    constructor(props) {
        super(props)
        this.state = {
            searchArea: "",
            searchType: "keyword",
            hasSubmit: false,
            results: []
        }
    }

    handleChange = event => {
        event.preventDefault();
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    handleSubmit = () => {
        this.setState({
            hasSubmit: true,
        });
    }

    render() {
        return (
            <div className="componentContainer">
                <div className="searchContainer">
                    <Form id="searchForm">
                        <Form.Control
                            type="textarea"
                            id="searchArea"
                            name="searchArea"
                            value={this.state.searchArea}
                            placeholder="recherche"
                            onChange={this.handleChange}
                            maxLength="100"
                        />
                        <Form.Control as="select" name="searchType" onChange={this.handleChange}>
                            <option value="keyword">Par mot-clé</option>
                            <option value="regex">Par RegEx</option>    
                        </Form.Control> 
    
                        <Button variant="dark" onClick={this.handleSubmit}>
                            Rechercher
                        </Button>
                    </Form>
                    <div id="results">
                    {
                        this.state.hasSubmit && this.state.results.length > 0?
                        (
                            <p>cc</p>
                        ):
                        (
                            <Alert id="noResults" variant="info">
                                <p>Aucun résultats trouvés, faites une recherche ou changez vos critères de recherche.</p>
                            </Alert>
                        )
                    }
                    </div>
                </div>
            </div>
        );
    }
}