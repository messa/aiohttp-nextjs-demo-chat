import React from 'react'
import { Form, Button, Message } from 'semantic-ui-react'

export default class SendForm extends React.Component {

  state = {
    message: '',
    sending: false,
    error: null,
  }

  handleChange = (e, { name, value }) => {
    this.setState({ [name]: value })
  }

  handleSubmit = async () => {
    const { message } = this.state
    if (!message) {
      return
    }
    this.setState({ sending: true })
    try {
      await this.props.onSubmit({ message })
      this.setState({ message: '', error: null, sending: false })
    } catch (err) {
      this.setState({ error: err.message, sending: false })
    }
  }

  render() {
    const { disabled, name } = this.props
    const { message, sending, error } = this.state
    return (
      <div className='SendForm'>
        <Form onSubmit={this.handleSubmit}>
          <Form.Group widths='equal'>
            <Form.Input
              fluid
              required
              name='message'
              value={message}
              onChange={this.handleChange}
              placeholder='Message'
              id='sendform-message'
              autoComplete="off"
              disabled={disabled || sending}
              loading={sending}
            />
            <Button
              color='orange'
              content='Send'
              disabled={disabled || !message}
            />
          </Form.Group>
        </Form>
        {error && (
          <Message negative>
            <Message.Header>Send failed</Message.Header>
            <p>{error}</p>
          </Message>
        )}
      </div>
    )
  }

}
