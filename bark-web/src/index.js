import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {FeedComponent, BarksComponent, BarkDetailComponent} from './barks'
import * as serviceWorker from './serviceWorker';

const appEl = document.getElementById('root')
if(appEl) {
  ReactDOM.render(<App />, appEl)
}

const e = React.createElement

const barksEl = document.getElementById("idBark")
if(barksEl) {
  ReactDOM.render(e(BarksComponent, barksEl.dataset), barksEl)
}

const barkFeedEl = document.getElementById("idBark-feed")
if(barkFeedEl) {
  ReactDOM.render(e(FeedComponent, barkFeedEl.dataset), barkFeedEl)
}

const barkDetailElements = document.querySelectorAll(".bark-detail")

barkDetailElements.forEach(container => {
  ReactDOM.render(e(BarkDetailComponent, container.dataset), container)
})

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
