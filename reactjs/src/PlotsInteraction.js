import React from 'react';
import { Scatter } from 'react-chartjs-2';

import {abs, range, pi, max} from 'mathjs';

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

class PlotsInteraction extends React.Component {
  render() {
    return(
      <Row>
        <Col md="5">
          <ClockPlot points={[{x: 0, y: 1}, {x: 0.2, y: 0.2}]} />
        </Col>
        <Col md="7">
          <Row>
            
          </Row>
        </Col>
      </Row>
    )
  }
}

export default PlotsInteraction
