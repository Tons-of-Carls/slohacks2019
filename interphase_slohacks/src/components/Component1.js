import React, { Component } from "react";
import { Spring } from "react-spring";

export class Component1 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      image: "",
      count:0,
      name:''
    };
    this.getImage = this.getImage.bind(this)
  }

  componentDidMount(){
    this.interval = setInterval(this.getImage, 400);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  getImage() {
    fetch('https://c59f92fa.ngrok.io/get_video', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    }).then((response) => {
      console.log(response)
      return response.json()
    }).then((data) => {
      const old_count = this.state.count
      this.setState({
        image:data['image'],
        count:old_count + 1
      })
    })
    console.log(this.state.count)
    if(this.state.count >= 6){
      fetch('https://c59f92fa.ngrok.io/authenticate', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      }).then((response) => {
        return response.json()
      }).then((data) => {
        this.setState({
          name:data['same'],
        })
      })
      this.setState({
        count:0
      })
    }
  }

  render(){
    return (
      <div>
        <Spring
          from={{ opacity: 0, marginLeft: -500 }}
          to={{ opacity: 1, marginLeft: 0 }}
        >
          {props => (
            <div style={props}>
              <div style={c1Style}>
                <h1>Security Camera</h1>
                <img src={"data:image/jpeg;base64,"+this.state.image} style={image}  />
              </div>
            </div>
          )}
        </Spring>
        <Spring
          from={{ opacity: 0, marginTop: -500 }}
          to={{ opacity: 1, marginTop: 0 }}
          config={{ delay: 1000 }}
        >
          {props => (
            <div style={props}>
              <div style={c2Style}>
                {this.state.name}
              </div>
            </div>
          )}
        </Spring>
      </div>
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

const image = {
  padding: "1.5rem",
  height: "400px",
  textAlign: "center",
  boxShadow: "0px 8px 1px #9E9E9E"
};

const c1Style = {
  background: "steelblue",
  color: "white",
  padding: "1.5rem",
  height: "600px",
  textAlign: "center",
  boxShadow: "0px 8px 1px #9E9E9E"
};

export default Component1;
