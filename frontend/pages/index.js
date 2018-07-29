import Link from 'next/link'
import Layout from '../components/Layout'
import LinkButton from '../components/LinkButton'

export default () => (
  <Layout>
    <h1>Chat demo</h1>
    <p>This is example chat app.</p>
    <LinkButton
      icon='sign in'
      color='red'
      href='/login'
      content='Login'
    />
  </Layout>
)
