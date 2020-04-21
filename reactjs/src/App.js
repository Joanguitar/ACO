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
import PlotsOnOff from "./PlotsOnOff.js"

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
                  <p>
                    This webpage's purpose is helping understanding the logic behind our channel estimation method.
                    You can also find more information in the paper and Github repository.
                  </p>
                  <h2 align="center">
                    Channel estimation from measurements
                  </h2>
                  <p align="right">
                    <a href="http://eprints.networks.imdea.org/1880/">Paper</a>
                  </p>
                  <p align="right">
                    <a href="https://github.com/Joanguitar/ACO">Github</a>
                  </p>
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
                <h3 align="center">
                  Analysis
                </h3>
                <p>
                  Let's for a second forget about the problem restrictions and consider the reference beam-pattern <InlineMath math="\bf{p}_0" /> and another one <InlineMath math="\bf{w}" />.
                  Let's now build another one that consists on the sum of both when <InlineMath math="\bf{w}" /> has its phase shifted by a unitary complex number as <InlineMath math="\alpha\bf{w}" />.
                  That's <InlineMath math="\bf{p}=\bf{h}_0+\alpha\bf{w}" />.
                  We plot its received signal strength.
                </p>
                <PlotsInteraction />
                <h3 align="center">
                  Plots
                </h3>
                <Row>
                  <Col md="4">
                    <h4 align="center">
                      Polar interaction
                    </h4>
                    <p>
                      The graph on the left depicts the complex polar representation of two beam-patterns' complex response.
                      The black one is the beam-pattern we are using for reference, thus it has zero phase.
                      This one is also unitary for representation purposes.
                    </p>
                  </Col>
                  <Col md="4">
                    <h4 align="center">
                      Received signal strength
                    </h4>
                    <p>
                      It's not hard to prove that the RSS of the combination of both beam-patterns when adding a phase shift to the one that's not for reference follows the wave fucntion depicted in the center graph.
                      This wave is pure with an offset and thus, its parameters (offset, width and phase offset) can be computed with a few points.
                    </p>
                  </Col>
                  <Col md="4">
                    <h4 align="center">
                      RSS's square root
                    </h4>
                    <p>
                      This plot on the right is interesting and it contains all the information we want.
                      The highest and lowest points are defined by the destructive and constructive interactions, thus the amplitude of both components can be retrieved.
                      The maximum possition indicates where the construction interaction happens, thus it indicates the phase of the second beam-pattern with a negative sign.
                    </p>
                  </Col>
                </Row>
                <h3 align="center">
                  Application to channel estimation
                </h3>
                <p>
                  This means that we can use those results to apply them to particullar antenna elements.
                  If in the reference beam-pattern and antenna is off, we can safely set <InlineMath math="\bf{w}" /> to be the beam-pattern with all antennas off except for the desired antenna.
                  Then we can set the phase shift to the ones allowed by the antenna constraints to compose 4 new beam-patterns that allow us to measure points in the RSS middle graph.
                  With those points we can reconstruct the whole wave and convert it to the right figure's RSS's square root to get that antenna's amplitude and phase.
                </p>
                <p>
                  There's a way to do the same for an antenna that's off by substracting it from the reference beam-pattern and then correcting the phase.
                  If you're interested on how to do it, please refer to the paper.
                </p>
                <p>
                  Now we simply need to apply this to all antennas we want to estimate.
                  And we have a channel (or sub-channel) estimation.
                  The choice of a subchannel depends on the will to reduce the number of required measurements.
                </p>
                <h2 align="center">
                  From channel estimation to beam-forming
                </h2>
                <p>
                  The next mission for the algorithm is to decide how to do the beam-forming with the channel estimation and the coefficient restrictions.
                </p>
                <Row>
                  <Col md="6">
                    <h4 align="center">
                      Phase
                    </h4>
                    <p>
                      We have to remember that the phase of the beam-pattern coefficients is restricted.
                      The easy solution to account for this quantization is to simply round to the closest value.
                      We take this approach not because it's the best, but because it's simple and it's out of the paper's scope.
                      There's an extense research on quantized beam-forming that can be used for this.
                    </p>
                  </Col>
                  <Col md="6">
                    <h4 align="center">
                      On or off?
                    </h4>
                    <p>
                      As for the phase, we are considering a simple strategy.
                      This strategy consists on optimizing assuming that the phase is unconstrained.
                      In the paper we prove this optimization's solution to be to switch on the strongest <InlineMath math="N" /> antennas that maximize <InlineMath math="\frac{\sum_{k=1}^N|a_k|}{\sqrt{N}}" />, where <InlineMath math="a_k" /> is the channel coefficient corresponding to the k-th strongest antenna.
                    </p>
                  </Col>
                </Row>
                <PlotsOnOff />
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default App;
