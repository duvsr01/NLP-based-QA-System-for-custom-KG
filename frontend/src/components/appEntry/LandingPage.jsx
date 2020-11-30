import React, { Component } from "react";
import { InputGroup, FormControl,Button, Col, Row } from "react-bootstrap";
import axios from "axios";

class LandingPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      question: "",
    };
  }

  handleSearchChange = e => {
    this.setState({
      question: e.target.value
    });
  };

  handleSubmit = e => {
    e.preventDefault();

    const data = {
      question: this.state.question
    };
    console.log("data is" + JSON.stringify(data));
    
    axios
    .post("http://127.0.0.1:5000/question", data)
    .then(response => {
      console.log("Status Code : ", response.status);
      console.log("Answer: "+response.data);
      })
    .catch(error => {
      console.log("Error: "+error);
    });
   
  };

  render() {
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
                value={this.state.question}
                onChange={this.handleSearchChange}
              />
              <Button 
              type="submit"
              variant="primary"
              value="Submit"
              onClick={this.handleSubmit}
              >Search</Button>
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
