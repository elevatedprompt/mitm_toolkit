import React from "react";
import Menu from "./layout/Menu";
import Content from "./layout/Content";
import Footer from "./layout/Footer";
import {Grid, Row} from "react-bootstrap";
require('../css/fullstack.css');

export default class App extends React.Component {
    render () {
        return (
            <Grid fluid={true}>
                <Row className="wrapper">
                    {this.props.user}
                    <Menu/>
                    <Content />
                </Row>
                <Footer/>
            </Grid>
        );
    }
}