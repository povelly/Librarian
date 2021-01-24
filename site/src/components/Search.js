import React, { Component } from "react";
import { Button, Form, Alert } from "react-bootstrap";
import axios from "axios";
import { Loading } from "./Loading";

import "../style/search.css"

export default class Search extends Component {

    constructor(props) {
        super(props)
        this.state = {
            searchArea: "",
            searchType: "keyword",
            results: [],
            suggestions: [],
            isLoading: false
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
    handleSubmit = async () => {
        this.setState({
            isLoading: true
        })
        try {
            let response = this.state.searchType === "regex" ? (await axios.get("http://127.0.0.1:8000/advanced-search", { params: { pattern: this.state.searchArea } })) : (await axios.get("http://127.0.0.1:8000/search", { params: { keyword: this.state.searchArea } }))

            // update state
            this.setState({
                isLoading: false,
                results: response.data,
                suggestions: []
            });
        } catch (e) {
            this.setState({
                isLoading: false
            })
        }

    }

    handleDownloadFile = async event => {
        const bookId = event.target.name.split(".")[0];
        let res = await axios.get("http://127.0.0.1:8000/book", { params: { id: bookId } });
        const bookText = res.data;
        // force the navigator to download the file
        var blob = new Blob([bookText], { type: 'text/plain' });
        var a = document.createElement('a');
        var url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = event.target.name // file name
        a.click();
        window.URL.revokeObjectURL(url);
    }

    render() {
        return (
            this.state.isLoading ? (
                <Loading />
            ) :
                (
                    <div className="componentContainer">
                        <div className="searchContainer">

                            <Form id="searchForm">
                                <Form.Control
                                    type="textarea"
                                    id="searchArea"
                                    name="searchArea"
                                    value={this.state.searchArea
                                    }
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
                                    this.state.results.length > 0 ?
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
                                                                        <a href="javascript:void(0)" onClick={this.handleDownloadFile} name={result.file}>{result.file}</a>
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
                                        ) :
                                        // si aucun résultats trouvés
                                        (
                                            <Alert id="noResults" variant="info">
                                                <p>Aucun résultats trouvés, faites une recherche ou changez vos critères de recherche.</p>
                                            </Alert>
                                        )
                                }
                            </div>
                        </div >
                    </div >
                )
        );
    }
}