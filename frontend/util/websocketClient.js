class WebsocketClient {

  socket = null
  subscriptions = {}
  nextSubscriptionId = 1

  connect() {
    if (this.socket) {
      return // already connected
    }
    const host = window.location.host
    const proto = window.location.protocol === 'http:' ? 'ws' : 'wss'
    const socket = new WebSocket(`${proto}://${host}/api/ws`)
    socket.onopen = () => {
      socket.send(JSON.stringify({
        type: 'subscribe',
      }))
    }
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.processMessage(data)
    }
    this.socket = socket
  }

  processMessage(data) {
    console.debug('WebsocketClient message:', data)
    if (data.type === 'messages') {
      const { messages } = data
      this.broadcast({
        type: 'messages',
        messages,
      })
    }
  }

  subscribe(callback) {
    const subscriptionId = this.nextSubscriptionId++
    this.subscriptions[subscriptionId] = callback
    return subscriptionId
  }

  unsubscribe(subscriptionId) {
    delete this.subscriptions[subscriptionId]
  }

  broadcast(data) {
    for (const key in this.subscriptions) {
      const callback = this.subscriptions[key]
      callback(data)
    }
  }

}

export default new WebsocketClient()
