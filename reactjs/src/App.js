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

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <h1 align="center">
          Adaptive Codebook Optimization
        </h1>
        <Row>
          <Col lg="12">
            <Card>
              <CardHeader>
                <CardTitle>
                  <h3 align="center">
                    Channel estimation from measurements
                  </h3>
                </CardTitle>
              </CardHeader>
              <CardBody>
                <Row>
                  <Col md="6">
                    <h4 align="center">
                      The problem
                    </h4>
                  </Col>
                  <Col md="6">
                    <h4 align="center">
                      Observation
                    </h4>
                  </Col>
                </Row>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default App;
