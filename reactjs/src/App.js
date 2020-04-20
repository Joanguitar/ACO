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

import PlotsInteraction from "./PlotsInteraction.js"

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
                    <p>
                      The problem consists on estimating the complex channel response as per antenna based on received signal strength.
                      The problem consists on two parts.
                      First building a codebook such that allows us to reconstruct the channel.
                      Second by reconstructing the channel using the measurements from the codebook.
                    </p>
                    <p>
                      If we denote <InlineMath math="\bf{h}" /> as the channel and <InlineMath math= "\bf{p}" /> as the measured beam-pattern.
                      We need to define a set <InlineMath math="\{\bf{p}_k\}" /> such that the set <InlineMath math="\{\bf{rss}_k\}" /> defined as <InlineMath math="\bf{rss}_k = |<\bf{h}, \bf{p}_k>|^2" /> let's you compute <InlineMath math="\bf{h}" />.
                    </p>
                    <p>
                      To be compliant with the existing low resolution hardware, the entries of each beampattern are restricted to <InlineMath math="\{0, 1, \bf{i}, -1, -\bf{i}\}" />.
                    </p>
                  </Col>
                  <Col md="6">
                    <h4 align="center">
                      Observation
                    </h4>
                    <p>
                      Note that the problem is theorically impossible to solve as any complex rotation of <InlineMath math="\bf{h}" /> would generate the same set of measurements regardless of the chosen codebook.
                      This can be solved by adding an additional condition to the problem that solve the angle uncertainty.
                      An example of this is assuming that the product with a reference beam-pattern has null complex angle.
                    </p>
                    <p>
                      This can be formulated as <InlineMath math="<\bf{h}, \bf{p}_0>\in\mathbb{R}^+" />.
                    </p>
                  </Col>
                </Row>
                <PlotsInteraction />
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default App;
