import React from 'react';
import { Scatter, Line } from 'react-chartjs-2';

import {abs, range, pi, max, cos, sin, sqrt} from 'mathjs';

// reactstrap components
import {
  Button,
  ButtonGroup,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardText,
  CardTitle,
  Label,
  FormGroup,
  Input,
  Table,
  Row,
  Col
} from "reactstrap";

import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import Slider from '@material-ui/core/Slider';
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

function valueLabelFormat(value){
  return(Math.round(value*180/pi)+'°')
}

class PlotsInteraction extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      amplitudes: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    }
    this.angle_domain = range(0, 2*pi, 0.01);
  }
  handle_amplitude = (event, amplitude) => {
    const amplitudes = this.state.amplitudes
    this.setState({
      amplitudes: amplitudes,
    })
  }
  render() {
    return(
      <>
      <Row>
        <Col md="2">
        </Col>
        <Col md="8">
          <Scatter
            data = {
              {
                datasets: [
                  {
                    label: 'RSS',
                    showLine: true,
                    lineTension: 0.1,
                    borderColor: "#1f8ef1",
                    borderWidth: 5,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointRadius: 4,
                    data: this.state.amplitudes.map((item, iter) => {return({x: iter, y: item})}),
                  }
                ]
              }
            }
            options = {{
              animation: {
                  duration: 0.5
              },
              legend: {
                display: false
              },
              tooltips: {
                enabled: false,
              },
              responsive: true,
              scales: {
                yAxes: [
                  {
                    gridLines: {
                      display: true,
                      drawBorder: false,
                      color: "rgba(255,255,255,0.1)",
                      zeroLineColor: "transparent"
                    },
                    ticks: {
                      min: 0,
                      max: 1,
                      fontColor: "#9a9a9a",
                      stepSize: 2,
                    }
                  }
                ],
                xAxes: [
                  {
                    gridLines: {
                      display: false,
                      drawBorder: false,
                      color: "rgba(255,255,255,0.1)",
                      zeroLineColor: "transparent"
                    },
                    ticks: {
                      enabled: false,
                      min: 0,
                      max: this.state.amplitudes.length-1,
                      fontColor: "#9a9a9a",
                      callback: () => {}
                    }
                  }
                ]
              }
            }}
          />
        </Col>
      </Row>
      <Row>
        {this.state.amplitudes.map((item, iter) => {return(
          <Col md="2">
            <FormLabel component="legend">
              {'Antenna ' + (iter+1)}
            </FormLabel>
            <Slider
              id={iter}
              value={item}
              onChange={this.handle_amplitude}
              aria-labelledby="continuous-slider"
              valueLabelDisplay="auto"
              min={0}
              max={1}
              step={0.01}
            />
          </Col>
        )})}
      </Row>
      </>
    )
  }
}

export default PlotsInteraction
