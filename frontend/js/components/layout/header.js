import React from "react";
import { Link, NavLink } from "react-router-dom"


export default class Header extends React.Component {
    render() {
        return (
            <React.Fragment>
                <div className="container d-none d-sm-block" style={{ textAlign: 'center' }}>
                    <p className="display-4 pt-3 pb-2">Richard Campen</p>
                </div>

                <nav className="navbar navbar-expand-sm navbar-light bg-light" style={{ backgroundColor: '#fafafa !important' }}>

                    <span className="mx-auto d-sm-none d-md-none d-lg-none d-xl-none" style={{ fontSize: '2rem', color: '#444444', fontWeight: 'lighter' }}>Richard Campen</span>


                    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#site-navbar" aria-controls="site-navbar" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon" />
                    </button>

                    <div className="collapse navbar-collapse" id="site-navbar">
                        <ul className="navbar-nav mx-auto">
                            <li className="nav-item">
                                <NavLink className="nav-link" exact to="/">ABOUT</NavLink>
                            </li>

                            <li className="nav-item">
                                <NavLink className="nav-link" to="/publications">PUBLICATIONS</NavLink>
                            </li>
                        </ul>
                    </div>
                </nav>
            </React.Fragment>
        )
    }
}
