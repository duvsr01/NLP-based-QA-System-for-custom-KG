import React, { Component } from "react";
import { InputGroup, FormControl,Button, Col, Row,Card,Container,Image,Navbar,Media,Form} from "react-bootstrap";
import axios from "axios";
import AutoCompleteText from "./AutoCompleteText";
import './AutoCompleteText.css';
import spartan_logo from "../images/spartan_logo.png"
import qa_logo from "../images/qa_system_logo.png"

class LandingPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      question: "",
      text:"",
      answer:"",
      suggestions:[],
    };
    this.onKeyUp = this.onKeyUp.bind(this);
    this.handleSubmit= this.handleSubmit.bind(this);
    this.suggestionSelected = this.suggestionSelected.bind(this);
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
    .post("http://127.0.0.1:5000/searchSuggestions",data) 
    .then(response => {
      let newSuggestions=[];
      console.log("Status Code : ", response.status);
      // console.log("Suggestions: "+response.data);
      let results = response.data
      for(let i in results){
        newSuggestions.push(results[i]);
      }
      // console.log("newSuggestions:"+newSuggestions);

      this.setState({
        suggestions:newSuggestions
      });
      })
    .catch(error => {
      console.log("Error: "+error);
    });
  };

  suggestionSelected (item){
    console.log("the suggested question is "+item);
    this.setState({
        question:item,
        suggestions:[],
    },() => {
      this.handleSubmit();
  })
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
      console.log("the bert question:",response.data.question);
      this.setState({
        answer:response.data
      })
      }else{
        this.setState({
          answer:"Did not find the answer for this question. Please try another one!"
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
            <li className="AutoCompleteText" key={item.suggestion} onClick={()=>this.suggestionSelected(item.suggestion)}>{item.suggestion}
             <Form.Text size="sm" className="text-muted" key={item.suggestion}>{item.tag}</Form.Text>
            </li>
            )}
        </ul>
        );
    }

    if(this.state.answer){
     content =
      <Container>
      <span className="d-block p-2 bg-primary text-white">
        Search Results:
      </span>
      <Card bg="white" style={{ width: "100%", margin: "0%", height: "250px"}}>
        <Card.Body>
          <Card.Title>{this.state.answer}</Card.Title>
        </Card.Body>
      </Card>
      </Container>
    }
    return (
      <Container fluid>
      <Navbar bg="light" expand="lg">
        <img
          src={spartan_logo}
          width="50"
          height="50"
          className="d-inline-block align-top"
          alt="Spartan logo"
        />
       </Navbar>
        <Container fluid> 
          <Row className="justify-content-md-center"> 
           <Col md={3}></Col>
            <Col>
              <Col md={8}>
              <Media className="justify-content-md-center">
                  <img
                  width={300}
                  height={280}
                  className="mr-2"
                  src={qa_logo}
                  alt="Spartan Logo Placeholder"
                />
              </Media>
              </Col>
              <Col xs={2} md={8}>
              <div>
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
                    {content}
                  </div>
              </div>

              </Col>
          </Col>
          </Row>
        </Container>
        </Container>  
    );
  }
}

export default LandingPage;