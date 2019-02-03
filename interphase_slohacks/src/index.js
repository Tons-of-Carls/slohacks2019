import React from "react";
import ReactDOM from "react-dom";
import { Transition, animated } from "react-spring";
import Component1 from "./components/Component1";

import "./styles.css";

class App extends React.Component {
  state = {
    showComponent3: false
  };

  toggle = e => this.setState({ showComponent3: !this.state.showComponent3 });

  render() {
    return (
      <div className="App">
        <Component1 />
      </div>
    );
  }
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
