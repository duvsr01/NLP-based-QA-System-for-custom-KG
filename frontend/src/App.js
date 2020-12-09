import React, { Component } from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import LandingPage from "./components/appEntry/LandingPage";
import "bootstrap/dist/css/bootstrap.css"; // To include React bootstrap's design.   https://react-bootstrap.github.io/getting-started/introduction/
import "font-awesome/css/font-awesome.css"; // To include font anwesome's design.     https://fontawesome.com/how-to-use/on-the-web/setup/using-package-managers
import "./App.css";

class App extends Component {
  render() {
    return (
      <main>
        <div className="content">
          <BrowserRouter>
            <Switch>
              <Route exact path="/" component={LandingPage} />
            </Switch>
          </BrowserRouter>
        </div>
      </main>
    );
  }
}

export default App;
