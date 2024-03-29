import React, { Component } from "react";

class Spinner extends Component {
  render() {
    return (
      <div className="spinner-border text-primary" role="status">
        <span className="sr-only">Searching...</span>
      </div>
    );
  }
}

export default Spinner;