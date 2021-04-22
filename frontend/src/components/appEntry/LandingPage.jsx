import React, { Component } from "react";
import { InputGroup, FormControl,Button, Col, Row,Card,Container } from "react-bootstrap";
import axios from "axios";
import AutoCompleteText from "./AutoCompleteText";
import './AutoCompleteText.css';

class LandingPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      question: "",
      answer:"",
      suggestions:[],
    };
    this.onKeyUp = this.onKeyUp.bind(this);
    this.handleSubmit= this.handleSubmit.bind(this);
    this.handleSearchChange = this.handleSearchChange.bind(this);
  }

  handleSearchChange = e => {
    this.setState({
      question: e.target.value
    });

  if(this.state.question.length<0) 
    return;

    const data = {
      question: this.state.question
    };
    console.log("data is" + JSON.stringify(data));

    axios
    .post("http://127.0.0.1:5000/suggestions",data) 
    .then(response => {
      let newSuggestions=[];
      console.log("Status Code : ", response.status);
      console.log("Suggestions: "+response.data);
      let results = response.data
      for(let i in results){
        newSuggestions.push(results[i]);
      }
      console.log("newSuggestions:"+newSuggestions);

      this.setState({
        suggestions:newSuggestions
      });
      })
    .catch(error => {
      console.log("Error: "+error);
    });
  };

  suggestionSelected (item){
    this.setState(()=>({
        question:item,
        suggestions:[],
    }))
}  

onKeyUp(event) {
  if (event.charCode === 13) {
   this.handleSubmit();
  }
}

  handleSubmit = e => {
    // e.preventDefault();

    const data = {
      question: this.state.question
    };
    console.log("data is" + JSON.stringify(data));
    axios
    .post("http://127.0.0.1:5000/question", data) 
    .then(response => {
      console.log("Status Code : ", response.status);
      console.log("Answer: "+response.data);
      if(Object.keys(response.data).length !== 0){
      this.setState({
        answer:response.data
      })
      }else{
        this.setState({
          answer:""
        })
      }
      })
    .catch(error => {
      console.log("Error: "+error);
    });

  };



  render() {
    let content;

    let displaySuggestions;
    const {suggestions,text} =  this.state;
    if(suggestions.length === 0){
        displaySuggestions= null;
    }
    else{
        displaySuggestions= (
            <ul className="AutoCompleteText" >
            {suggestions.map((item)=>         
            <li className="AutoCompleteText" key={item} onClick={()=>this.suggestionSelected(item)}>{item}</li>)}
        </ul>

        );
    }

    if(this.state.answer){
     content =
      <div>
      <Card bg="white" style={{ width: "100%", margin: "1%", height: "500px"}}>
      <Card.Body>
      <Card.Title>{this.state.answer}</Card.Title>
      </Card.Body>
      </Card>
      </div>
    }
    return (
      <div className="mx-auto" style={{ width: "900px"}} >  
      <div className=" container">
        <div className="row">
        </div>
      <div style={{ height: "75vh" }} className="container valign-wrapper ">
        <div className="container border rounded p-5">
          <div>
            <h3 className="text-left text-black  font-family-sans-serif background indigo">
              {" "}
              Welcome to our Question Answering System
            </h3>
          </div>
          <div>
            <br />

          <div className="input-group">
            <input className="form-control border-end-0 border" 
                type="text"  
                placeholder="Enter Search Query!" 
                id="example-search-input"
                value={this.state.question}
                onChange={this.handleSearchChange}
                onKeyPress={this.onKeyUp}
            />
            
            <div className="input-group-append">
              <button className="btn btn-secondary" type="button"  onClick={this.handleSubmit} >
                <i className="fa fa-search"></i>
              </button>
            </div>
            {displaySuggestions}
            </div>
            
            <br />
            <div>
              <span className="d-block p-2 bg-primary text-white">
                Search Results:
              </span>
              {content}
            </div>
          </div>
        </div>
      </div>
      </div>
      </div> 
    );
  }
}

export default LandingPage;