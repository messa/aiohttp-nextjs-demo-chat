import React from 'react'
import { Loader, Message, Dimmer } from 'semantic-ui-react'

const cache = {}

export default function fetchWrapper(WrappedComponent, urlFactory, optionsFactory) {
  return class extends React.Component {

    state = {
      data: null,
      cached: false,
      loading: true,
      laoded: false,
      error: null,
    }

    componentDidMount() {
      this.loadData()
    }

    async loadData() {
      try {
        const url = urlFactory(this.props)
        const options = optionsFactory ? optionsFactory(this.props) : {
          credentials: 'same-origin',
          headers: {
            'Accept': 'application/json',
          },
        }
        const cacheKey = JSON.stringify({ url, options })
        console.debug('cacheKey:', cacheKey)
        if (cache[cacheKey]) {
          this.setState({
            data: cache[cacheKey],
            cached: true,
          })
        }
        const r = await fetch(url, options)
        if (r.status != 200) {
          const text = await r.text()
          throw new Error(`Status code: ${r.status}: ${text.substr(0, 1000)}`)
        }
        const data = await r.json()
        cache[cacheKey] = data
        this.setState({
          data,
          loaded: true,
          cached: false,
          loading: false,
          error: null,
        })
      } catch (err) {
        this.setState({
          loading: false,
          error: err.message.toString(),
        })
      }
    }

    render() {
      const error = !this.state.error ? null : (
        <Message negative>
          <Message.Header>Load failed</Message.Header>
          <p>{this.state.error}</p>
        </Message>
      )
      const wrapped = (!this.state.loaded && !this.state.cached) ? null : (
        <WrappedComponent
          data={this.state.data}
          cached={this.state.cached}
          {...this.props}
        />
      )
      return (
        <Dimmer.Dimmable dimmed={this.state.loading}>
          {error}
          {wrapped}
          {!error && !wrapped && (
            <img
              src='https://react.semantic-ui.com/images/wireframe/paragraph.png'
              style={{ width: 312, height: 106 }}
            />
          )}
          <Dimmer active={this.state.loading} inverted>
            <Loader inline='centered'>Loading</Loader>
          </Dimmer>
        </Dimmer.Dimmable>
      )
    }
  }
}
