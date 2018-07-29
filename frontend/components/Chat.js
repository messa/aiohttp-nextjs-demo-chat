import React from 'react'
import fetchWrapper from '../util/fetchWrapper'
import SendForm from './SendForm'
import wsClient from '../util/websocketClient'

function formatMessageDate(dtStr) {
  const dt = new Date(dtStr)
  return `${dt.getHours()}:${dt.getMinutes()}`
}

const Message = ({ message }) => (
  <div id={message.id}>
    {formatMessageDate(message.date)}
    {' '}
    <strong>{message.author.name}:</strong>
    {' '}
    {message.body}
  </div>
)

class ChatView extends React.Component {

  wsClientSubscriptionId = null
  state = {
    messages: null,
  }

  componentDidMount() {
    wsClient.connect()
    if (!this.wsClientSubscriptionId) {
      this.wsClientSubscriptionId = wsClient.subscribe(data => {
        if (data.type === 'messages') {
          const { messages } = data
          this.setState({ messages })
        }
      })
    }
  }

  componentWillUnmount() {
    if (this.wsClientSubscriptionId) {
      this.wsClient.unsubscribe(this.wsClientSubscriptionId)
      this.wsClientSubscriptionId = null
    }
  }

  handleSendSubmit = async ({ message }) => {
    const payload = {
      body: message,
    }
    const r = await fetch('/api/send-message', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin',
      body: JSON.stringify(payload),
    })
    if (r.status != 200) {
      throw new Error(`Got status code ${r.status}`)
    }
    const { messages } = await r.json()
    this.setState({
      messages
    })
  }

  render() {
    const { data, cached } = this.props
    const { user } = data
    const messages = this.state.messages || data.messages
    return (
      <div className='ChatView'>
        {messages.map(msg => (
            <Message key={msg.id} message={msg} />
        ))}
        <SendForm
          name={user.name}
          disabled={cached}
          onSubmit={this.handleSendSubmit}
        />
      </div>
    )
  }
}

export default fetchWrapper(ChatView, () => '/api/chat')
