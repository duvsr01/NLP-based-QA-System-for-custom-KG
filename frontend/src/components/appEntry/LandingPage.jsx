import React, { Component } from "react";
import { InputGroup, FormControl, Col, Row } from "react-bootstrap";
import axios from "axios";

class LandingPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchText: "",
    };
  }

  render() {
    console.log(this.state.searchText);
    return (
      <div style={{ height: "75vh" }} className="container valign-wrapper ">
        <div className="container border rounded p-5">
          <div>
            <h3 className="text-left text-black font-italic font-family-sans-serif">
              {" "}
              Welcome to our Question Answering System
            </h3>
          </div>
          <div>
            <br />
            <InputGroup className="mb-3 col-sm-10">
              <FormControl
                placeholder="Enter Search Query!"
                value={this.state.searchText}
              />
            </InputGroup>
            <br />
            <div>
              <span className="d-block p-2 bg-primary text-white">
                Search Results:
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default LandingPage;
