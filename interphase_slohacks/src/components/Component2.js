import React, { Component } from "react";
import { Spring } from "react-spring";

export class Component2 extends Component {
  handleClick1() {}

  render() {
    //variable will change its value when corresponding button is pressed
    var carl = false;
    var kev = false;
    var juy = false;

    return (
      <Spring
        from={{ opacity: 0, marginTop: -500 }}
        to={{ opacity: 1, marginTop: 0 }}
        config={{ delay: 1000 }}
      >
        {props => (
          <div style={props}>
            <div style={c2Style}>
              <button style={btn1} onClick={this.props.toggle}>
                {" "}
                Carleton{" "}
              </button>
              <button style={btn2} onClick={this.props.toggle}>
                {" "}
                Kevin{" "}
              </button>
              <button style={btn3} onClick={this.props.toggle}>
                {" "}
                Juyeong{" "}
              </button>
            </div>
          </div>
        )}
      </Spring>
    );
  }
}

const c2Style = {
  background: "slateblue",
  color: "white",
  padding: "1.5rem",
  boxShadow: "0px 8px 1px #9E9E9E",
  textAlign: "center"
};

const btn1 = {
  background: "#333",
  color: "#fff",
  padding: "1rem 2rem",
  border: "none",
  textTransform: "uppercase",
  margin: "15px 0"
};

const btn2 = {
  background: "#333",
  color: "#fff",
  padding: "1rem 2rem",
  border: "none",
  textTransform: "uppercase",
  margin: "15px 0",
  marginLeft: "20%",
  marginRight: "20%"
};

const btn3 = {
  background: "#333",
  color: "#fff",
  padding: "1rem 2rem",
  border: "none",
  textTransform: "uppercase",
  margin: "15px 0"
};

const identify = {
  textAlign: "left",
  textAlignVertical: "center"
};

export default Component2;
