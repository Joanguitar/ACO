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
      th: 0.5
    }
    this.angle_domain = range(0, 2*pi, 0.01);
  }
  handle_amplitude = (amplitude, iter) => {
    var amplitudes = this.state.amplitudes
    amplitudes[iter] = amplitude

    const sorted_amplitudes = amplitudes.slice().sort(function(a, b){return b-a})
    var sorted_amplitudes_cumsum = []
    sorted_amplitudes.reduce(function(a,b,i) { return sorted_amplitudes_cumsum[i] = a+b; },0);
    var term = sorted_amplitudes_cumsum.map((item, iter) => item/sqrt(iter+1))

    var ii_term = 0
    var max_term = 0
    term.forEach((item, i) => {
      if(item > max_term) {
        max_term = item;
        ii_term = i
      }
    });

    const th = sorted_amplitudes[ii_term];

    this.setState({
      amplitudes: amplitudes,
      th: th,
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
                    label: 'On',
                    showLine: false,
                    lineTension: 0.1,
                    borderColor: "#1ffe11",
                    borderWidth: 5,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointRadius: 4,
                    data: this.state.amplitudes.map((item, iter) => {return((item >= this.state.th && {x: iter, y: item}))}),
                  },
                  {
                    label: 'Off',
                    showLine: false,
                    lineTension: 0.1,
                    borderColor: "#ff1e11",
                    borderWidth: 5,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointRadius: 4,
                    data: this.state.amplitudes.map((item, iter) => {return((item < this.state.th && {x: iter, y: item}))}),
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
                      max: this.state.amplitudes.length-0.9,
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
              value={item}
              onChange={(event, value) => this.handle_amplitude(value, iter)}
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
