import React from "react";

import Layout from "../../components/layout/index"


const API_ENDPOINT = '/api/v2/pages/?type=app.AboutPage&fields=bio'

export default class AboutPage extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            'title': '',
            'bio': '',
        }

    }

    componentDidMount() {

        // TODO: persist this somewhere better.. redux?
        this.loadPageData(API_ENDPOINT)
            .then(data => this.setState({
                'title': data.items[0].title,
                'bio': data.items[0].bio
            }))
    }

    render() {

        const { title, bio } = this.state;

        return (
            <Layout>

                <div className="py-3">
                    <h3 className="pt-2">{ title }</h3>
                </div>

                <p className="py-3 px-3">
                    <img className="rounded-circle" src="https://secure.gravatar.com/avatar/de5821b0f24012e7c48b659e97e19bb7?s=200" style={{ width: '150px', height: '150px' }}/>
                </p>

                <p className="pt-3 pb-2 px-3">
                    { bio }
                </p>

                <br/>
                <br/>

                <p>
                    LINKS
                </p>

            </Layout>
        );
    }

    loadPageData(endpoint) {
        return fetch(endpoint)
            .then(response => response.json())
    }

}
