import React, {Component} from "react";


export default class Footer extends Component {
    render() {
        return (
            <footer className="footer pb-1 pt-3 text-center">
                <p id='copyright'>
                    <small>
                        Copyright &#169 2017 <a href="/">Richard Campen</a>
                    </small>
                </p>
            </footer>
        )
    }
}
