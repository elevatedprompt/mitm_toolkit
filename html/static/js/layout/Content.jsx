import React from "react";
import { Button, Grid, Row, Col } from "react-bootstrap";
import BotList from "../BotList";
import Command from "../Command";

export default class Content extends React.Component {
    render () {
        return (
            <Grid fluid={true}>
                <Row>
                    <Col md={2} className="bot-list">
                        <BotList title="Bot List!"/>
                    </Col>

                    <Col md={10} className="content">
                        <Command/>
                    </Col>
                </Row>
            </Grid>
        )
      }
}