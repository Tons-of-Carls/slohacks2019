import React, { Component } from "react";
import { Spring } from "react-spring";

export class Component2 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isHovering: false
    };
  }

  toggleHover() {
    this.setState({ isHovering: !this.state.isHovering });
  }

  render() {
    var divStyle;
    if (this.state.isHovering) {
      divStyle = c2Hover;
    } else {
      divStyle = c2Style;
    }

    return (
      <Spring
        from={{ opacity: 0, marginTop: -500 }}
        to={{ opacity: 1, marginTop: 0 }}
        config={{ delay: 1000 }}
      >
        {props => (
          <div style={props}>
            <div
              style={divStyle}
              onMouseEnter={this.toggleHover}
              onMouseLeave={this.toggleHover}
              onClick={this.props.toggle}
            >
              <h1 style={identify}>Identify</h1>
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
  padding: "1.5rem"
};

const btn = {
  background: "#333",
  color: "#fff",
  padding: "1rem 2rem",
  border: "none",
  textTransform: "uppercase",
  margin: "15px 0"
};

const c2Hover = {
  background: "mediumslateblue",
  color: "white",
  padding: "1.5rem"
};

const identify = {
  textAlign: "center"
};

export default Component2;
