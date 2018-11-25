import React, {Component} from "react";

import Header from "./header"
import Footer from "./footer"


export default class Layout extends Component {
    render() {
        return (
            <div>
                <Header/>
                <div className="container main-content">
                    <div className="row">
                        <div className="col-9 mx-auto" style={{ textAlign: 'center' }}>
                            <hr/>
                            {this.props.children}
                        </div>
                    </div>
                </div>
                <Footer />
            </div>
        )
    }
}