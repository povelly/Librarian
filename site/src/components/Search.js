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
            results: [],
            suggestions: []
        }
    }

    // appelée lors d'un evenement sur un element du formulaire
    handleChange = event => {
        event.preventDefault();
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    // appelée lors de l'envoie du formulaire
    handleSubmit = () => {
        // bouchons
        let res = []
        for (let i = 1; i <= 50; i++)
            res.push("res_book_number_" + i);
        let sugs = []
        for (let i = 1; i <= 5; i++)
            sugs.push("sug_book_number_" + i);

        // update state
        this.setState({
            hasSubmit: true,
            results: res,
            suggestions : sugs
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

                    <div id="resultsZone">
                    {
                        // si la requete de recherche a été envoyé et que des resultats ont été trouvés
                        this.state.hasSubmit && this.state.results.length > 0?
                        (
                            <div id="resultsAndSuggestions">
                                <div id="resultsGroup">
                                    <div>Resultats:</div>
                                    <div id="results">
                                        {
                                            // affichage des résultats
                                            this.state.results.map((result, i) => {
                                                return (
                                                    <div key={i}>
                                                        {result}
                                                    </div>
                                                );
                                            })
                                        }
                                    </div>   
                                </div>

                                <div id="suggestionsGroup">
                                    <div>Suggestions:</div>
                                    <div id="suggestions">
                                        {
                                            // affichage des suggestions
                                            this.state.suggestions.map((suggestion, i) => {
                                                return (
                                                    <div key={i}>
                                                        {suggestion}
                                                    </div>
                                                );
                                            })
                                        }
                                    </div>
                                </div>
                            </div>
                        ):
                        // si aucun résultats trouvés
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