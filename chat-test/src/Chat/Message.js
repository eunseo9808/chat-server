import React, { Component } from 'react';
import PropTypes from 'prop-types'


const Message = ({user_words, musio_words}) => (
  <div >
    <div>
      {user_words}
    </div>
  </div>
)

Message.propTypes = {
  user_words: PropTypes.string.isRequired,
}


export default Message;
