import React from "react";
import { FormGroup, ControlLabel, FormControl, Button, Grid, Row, Col, Checkbox } from "react-bootstrap";

var $ = require('jquery');

export default class BotList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            title: 'MITM - ' + this.props.title,
            bots: {}
        };
        // This binding is necessary to make `this` work in the callback
        this.getPythonBots = this.getPythonBots.bind(this);

        // Load data from API
        this.getPythonBots();
    }

    setBotdata(data) {
        this.setState(
            {
                bots: data
            }
        );
    }

    /**
     * Request bot list from API
     */
    getPythonBots() {
        $.get(window.location.href + 'bots', (data) => {
            console.log(data);
            this.setBotdata(data);
        });
    }

    render () {
        return (
            <Grid fluid={true}>
                <Row>
                    <Col md={12}>
                        <form>
                            <FormGroup controlId="formControlsSelectMultiple">
                                <ControlLabel>{this.state.title}</ControlLabel>
                                {Object.keys(this.state.bots).map((key, i) => 
                                   <Checkbox readOnly key={i}> {key}: {this.state.bots[key]}</Checkbox>
                                )}
                            </FormGroup>
                            <Button type="button" bsStyle="danger">Terminate c2! variable </Button>
                            <Button type="button" bsStyle="warning">Terminate Selected  Bots</Button>
                        </form>
                    </Col>
                </Row>
            </Grid>
        )
      }
}