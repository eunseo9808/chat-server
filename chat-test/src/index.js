import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import { Provider } from 'react-redux'
import  Reducer from './Chat/Reducer'
import { createStore, applyMiddleware } from 'redux'
import Chat from './Chat/Chat';
import registerServiceWorker from './registerServiceWorker'
import thunk from 'redux-thunk';

const store = createStore(Reducer, applyMiddleware(thunk));

ReactDOM.render(
  <Provider store = {store}>
      <Chat messages={[]}/>
  </Provider>,
   document.getElementById('root'));
registerServiceWorker();
