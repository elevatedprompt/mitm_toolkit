import React from "react";
import { Button, Grid, Row, Col } from "react-bootstrap";

export default class Hello extends React.Component {
    render () {
        return (
            <Grid>
                <Row>
                    <Col md={12}>
                        My Header
                    </Col>
                </Row>
            </Grid>
        )
      }
}