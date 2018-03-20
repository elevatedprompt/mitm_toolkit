import React from "react";
import { Button, Grid, Row, Col } from "react-bootstrap";

export default class Footer extends React.Component {
    render () {
        return (
            <Grid fluid={true}>
                <Row>
                <Col>
                    <footer className="footer">
                        <div>
                            <span className="text-muted">Some Stuff here</span>
                        </div>
                    </footer>
                </Col>
                </Row>
            </Grid>
        )
      }
}

