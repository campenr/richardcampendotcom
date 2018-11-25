import React from 'react'
import ReactDOM from 'react-dom'

import { BrowserRouter, Route, Switch } from 'react-router-dom'

import AboutPage from "./components/pages/aboutPage";
import PublicationsPage from "./components/pages/publicationsPage";

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../scss/main.scss';


const App = () => (
  <BrowserRouter>
      <React.Fragment>
        <Route exact path='/' component={AboutPage} />
        <Route path='/publications' component={PublicationsPage} />
      </React.Fragment>
  </BrowserRouter>
)


ReactDOM.render(
  <App />,
  document.getElementById('react-root')
);
