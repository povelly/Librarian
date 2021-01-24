import React, { Component } from "react";
import { Spinner } from "react-bootstrap";

import "../style/loading.css";

export class Loading extends Component {

  render() {
    return (
      <div className="loadingMain">
        <Spinner animation="border"></Spinner>
      </div>
    )
  }

}