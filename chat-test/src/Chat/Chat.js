import React, { Component } from 'react';
import ChatList from './ChatList'
import axios from 'axios'
import { getMessages, set_bind,addMessage } from './action'
import { connect } from 'react-redux'


class Chat extends Component {
  constructor(props){
    super(props)
    this.state = this.props
    this.onSendClick = this.onSendClick.bind(this)
    this.registToken = this.registToken.bind(this)
    this.props.getMessages()
    this.scrollToBottom = this.scrollToBottom.bind(this);
  }

  scrollToBottom = () => {
    if(this.state.token !== undefined){
      this.messagesEnd.scrollIntoView({ behavior: "smooth" });
    }
  }

  componentWillUpdate(nextProps, nextState) {
    if(nextState.token !== undefined){
      const options = {
        headers:{
          "authorization": "Bearer " + nextState.token
        }
      }
      this.connection = new WebSocket('ws://127.0.0.1:8000/ws/chatrooms/1/',[], options);

      this.connection.onmessage = (e) => {
        var data = JSON.parse(e.data);
        console.log(this.state)
        // socket.on('message', msg => {this.props.addMessage(msg)});
        this.state.addMessage(data)
      }

      this.connection.onclose = function(e) {
          console.error('Chat socket closed unexpectedly');
      };
    }
  }

  componentDidMount() {
    this.scrollToBottom();
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }

  onSendClick(e){
    e.preventDefault()
    this.message = e.target.chat_input.value
    this.connection.send(JSON.stringify({
            'message': this.message,
            'token': this.state.token
    }));
  }

  registToken(e){
    e.preventDefault()
    const token = e.target.token_input.value

    this.setState({token: token})

  }

  render() {
    if(this.state.token === undefined){
      return (
        <div >
            <form onSubmit={this.registToken}>
              <input id="token_input" type="text" size="100" placeholder="TOKEN"/><br/>
              <input id="token-submit" type="submit"/>
            </form>
        </div>
      );
    }
    else{
      return (
        <div >
          <ChatList messages={this.props.messages}/>

          <div style={{ float:"left", clear: "both" }}
               ref={(el) => { this.messagesEnd = el; }}>
          </div>
          <div>
            <form onSubmit={this.onSendClick}>
              <input id="chat_input" type="text" size="100"/><br/>
              <input id="chat-message-submit" type="submit"/>
            </form>
          </div>
        </div>
      );
    }
  }
}

const mapStateToProps = state => {

  if(state === undefined) return {messages: []}
  return { messages: state.messages }
}
const mapDispatchToProps = (dispatch) => {
    return {
        getMessages: () => dispatch(getMessages()),
        addMessage: (msg) => dispatch(addMessage(msg)),
        set_bind: () => dispatch(set_bind())
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(Chat)
