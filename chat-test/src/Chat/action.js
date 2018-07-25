import axios from 'axios'
import io from 'socket.io-client';

const ADD_MESSAGE = 'ADD_MESSAGE';
const GET_MESSAGES = 'GET_MESSAGES';
const SET_BIND = 'SET_BIND';
const SERVER_URL = 'http://127.0.0.1:8000'

export function getMessages(){
  return (dispatch) => {
    /*
            axios.get(SERVER_URL)
              .then(function (response) {

                dispatch({
                  type: GET_MESSAGES,
                  data: response.data.data,
                })
              })
              */
              dispatch({
                type: GET_MESSAGES,
                data: [],
              })
          }

}

export function addMessage(message){
  return (dispatch) => {
    dispatch({
      type: ADD_MESSAGE,
      data: message
    })
  }
}

export function set_bind(){
  const socket = io.connect('http://localhost:8000');
  socket.on('user message', msg => addMessage(msg));

  return (dispatch) => {
    dispatch({
      type: SET_BIND,
      data: socket
    })
  }
}
