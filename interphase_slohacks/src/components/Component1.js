import React from "react";
import { Spring } from "react-spring";

export default function Component1() {
  return (
    <Spring
      from={{ opacity: 0, marginLeft: -500 }}
      to={{ opacity: 1, marginLeft: 0 }}
    >
      {props => (
        <div style={props}>
          <div style={c1Style}>
            <h1>Who is this?</h1>
            <p>insert image/video</p>
          </div>
        </div>
      )}
    </Spring>
  );
}

const c1Style = {
  background: "steelblue",
  color: "white",
  padding: "1.5rem",
  height: "400px",
  textAlign: "center"
};
