import { combineReducers } from 'redux'

const MessageReducer = (state = [], action) => {
  switch(action.type){
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages:  [...state.messages, {'user_words': action.data['message']}]
      }
    case 'GET_MESSAGES':
      return {
        ...state,
        messages: action.data
      }
  }
}

const SocketIOReducer = (state = [], action) => {
  switch(action.type){
    case 'SET_BIND':
      return {
        ...state,
        socketIO: action.data
      }
  }
}


export default MessageReducer
