import React, { Component } from "react";
import { Spring } from "react-spring";

export class Component3 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isCorrect: false
    };
  }

  render() {
    var putAnswer;
    if (this.state.isCorrect) {
      putAnswer = correct;
    } else {
      putAnswer = incorrect;
    }

    return (
      <div style={correct}>
        <h1>Correct</h1>
      </div>
    );
  }
}

const correct = {
  background: "darkseagreen",
  color: "white",
  padding: "1.5rem 1.5rem 5rem 1.5rem",
  textAlign: "center"
};

const incorrect = {
  background: "crimson",
  color: "white",
  padding: "1.5rem 1.5rem 5rem 1.5rem",
  textAlign: "center"
};

export default Component3;
