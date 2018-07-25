import React, { Component } from 'react';
import PropTypes from 'prop-types'
import Message from './Message'

const ChatList = ({messages}) => (
  <div>
    {
      messages.map((message, i) => (
        <Message key={i} {...message}/>
      ))
    }
  </div>
)

ChatList.propTypes = {
  messages: PropTypes.arrayOf(
    PropTypes.shape(Message.propTypes)
  ),
}


export default ChatList;
