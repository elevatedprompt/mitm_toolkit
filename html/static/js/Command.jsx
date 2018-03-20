import React from "react";
import { Nav, NavItem, Grid, Row, Col, FieldGroup, FormGroup, FormControl, Button, Panel} from "react-bootstrap";

export default class Command extends React.Component {
    render () {
        return (
            <Grid fluid={true}>
                <Row>
                    <Col md={12}>
                        <Nav bsStyle="pills" activeKey={1}>
                            <NavItem eventKey={1} href="/home">
                                DNS
                            </NavItem>
                            <NavItem eventKey={2} title="Item">
                                SMTP
                            </NavItem>
                            <NavItem eventKey={3} disabled>
                                FTP
                            </NavItem>
                        </Nav>
                        <br/>
                        <Panel bsStyle="primary">
                            <Panel.Heading>
                                <Panel.Title componentClass="h3">DNS Spoof</Panel.Title>
                            </Panel.Heading>
                            <Panel.Body>
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tempor magna a felis tempus, vitae sagittis elit blandit. Vestibulum iaculis tincidunt purus. In sit amet odio nulla. Aenean neque purus, hendrerit posuere pellentesque sed, sodales eu nisi. Phasellus pharetra tincidunt quam. Vivamus malesuada, odio pellentesque sodales feugiat, erat ligula venenatis turpis, quis aliquam velit elit ut tortor. In dignissim dictum tellus nec ultricies. Nullam tempus eu justo sed egestas. Etiam et malesuada orci. Maecenas viverra pellentesque est, in feugiat ex interdum a. Morbi ultricies porttitor nulla, at aliquet tortor ultrices vitae.
                            </Panel.Body>
                        </Panel>
                        <form>
                            <FormGroup controlId="formBasicText">
                                <FormControl
                                type="text"
                                value=""
                                placeholder="google.com"
                            /></FormGroup>
                            <FormGroup controlId="formBasicText">
                                <FormControl
                                type="text"
                                value=""
                                placeholder="1.2.3.4"
                            /></FormGroup>
                            <Button type="button" bsStyle="success">Send it!</Button>
                        </form>
                    </Col>
                </Row>
            </Grid>
        )
      }
}