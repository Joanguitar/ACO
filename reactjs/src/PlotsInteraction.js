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

import ClockPlot from './functions/ClockPlot.js'

function valueLabelFormat(value){
  return(Math.round(value*180/pi)+'°')
}

class PlotsInteraction extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      amplitude: 0.8,
      phase: 0.25*pi,
    }
    this.angle_domain = range(0, 2*pi, 0.01);
  }
  handle_amplitude = (event, amplitude) => {
    this.setState({
      amplitude: amplitude,
    })
  }
  handle_phase = (event, phase) => {
    this.setState({
      phase: phase,
    })
  }
  render() {
    const rss = this.angle_domain.map(item => {return(1+this.state.amplitude**2+2*this.state.amplitude*cos(item+this.state.phase))})
    const amp = rss.map(item => {return(sqrt(item))})
    return(
      <>
      <Row>
        <Col md="2">
          <ClockPlot points={[{x: 1, y: 0}, {x: this.state.amplitude*cos(this.state.phase), y: this.state.amplitude*sin(this.state.phase)}]} />
        </Col>
        <Col md="5">
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
                    pointRadius: 0,
                    data: rss.toArray().map((item, iter) => {return({x: iter, y: item})}),
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
                      max: 4,
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
                      max: rss.length,
                      fontColor: "#9a9a9a",
                      callback: () => {}
                    }
                  }
                ]
              }
            }}
          />
        </Col>
        <Col md="5">
          <Scatter
            data = {
              {
                datasets: [
                  {
                    label: 'AMP',
                    showLine: true,
                    lineTension: 0.1,
                    borderColor: "#1f8ef1",
                    borderWidth: 5,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointRadius: 0,
                    data: amp.toArray().map((item, iter) => {return({x: iter, y: item})}),
                  }
                ]
              }
            }
            options = {{
              animation: {
                  duration: 0
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
                      max: 4,
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
                      max: rss.length,
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
        <Col md="4">
        </Col>
        <Col md="2">
          <FormLabel component="legend">
            Amplitude
          </FormLabel>
          <Slider
            value={this.state.amplitude}
            onChange={this.handle_amplitude}
            aria-labelledby="continuous-slider"
            valueLabelDisplay="auto"
            min={0}
            max={1}
            step={0.01}
          />
        </Col>
        <Col md="2">
          <FormLabel component="legend">
            Phase
          </FormLabel>
          <Slider
            value={this.state.phase}
            onChange={this.handle_phase}
            aria-labelledby="continuous-slider"
            valueLabelDisplay="auto"
            getAriaValueText={valueLabelFormat}
            valueLabelFormat={valueLabelFormat}
            min={0}
            max={2*pi}
            step={0.01}
          />
        </Col>
      </Row>
      </>
    )
  }
}

export default PlotsInteraction
