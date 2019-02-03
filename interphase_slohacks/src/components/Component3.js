import React, { Component } from "react";
import { Spring } from "react-spring";

export class Component3 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isCorrect: false
    };
  }

  //should reference the variable from component2 carl,kev,and juy
  //if the reference variable matched with the image, isCorrect is True
  authenticate() {
    //if the result matches the name make isCorrect True
    //else isCorrect is False
  }

  render() {
    var putAnswer;
    if (this.state.isCorrect) {
      putAnswer = correct;
      return (
        <div style={putAnswer}>
          <h1>Correct</h1>
        </div>
      );
    } else {
      putAnswer = incorrect;
      return (
        <div style={putAnswer}>
          <h1>Incorrect</h1>
        </div>
      );
    }
  }
}

const correct = {
  background: "darkseagreen",
  color: "white",
  padding: "1.5rem 1.5rem 2.5rem 1.5rem",
  flex: 1,
  justifyContent: "center",
  alignText: "center",
  boxShadow: "0px 8px 1px #9E9E9E"
};

const incorrect = {
  background: "crimson",
  color: "white",
  padding: "1.5rem 1.5rem 2.5rem 1.5rem",
  flex: 1,
  justifyContent: "center",
  textAlign: "center",
  boxShadow: "0px 8px 1px #9E9E9E"
};

export default Component3;
