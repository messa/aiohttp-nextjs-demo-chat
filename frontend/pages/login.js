import { Button } from 'semantic-ui-react'
import Layout from '../components/Layout'
import fetchWrapper from '../util/fetchWrapper'

const LoginButtonsView = ({ data }) => (
  <div className='loginButtons'>
    {data.fb && (
      <Button
        color='facebook'
        icon='facebook'
        content='Sign in via Facebook'
        href='/auth/facebook'
      />
    )}
    {data.google && (
      <Button
        color='google plus'
        icon='google'
        content='Sign in via Google'
        href='/auth/google'
      />
    )}
    {data.dev && (
      <div>
        <Button
          color='grey'
          icon='sign in'
          content='Sign in as dev user 1'
          href='/auth/dev?name=dev+user+1'
        />
        <Button
          color='grey'
          icon='sign in'
          content='Sign in as dev user 2'
          href='/auth/dev?name=dev+user+2'
        />
      </div>
    )}
    <style jsx>{`
      .loginButtons :global(.ui.button) {
        margin-bottom: 1rem;
        margin-right: 10px;
      }
    `}</style>
  </div>
)

const LoginButtons = fetchWrapper(LoginButtonsView, (props) => '/auth/methods')

export default () => (
  <Layout>
    <h1>Login</h1>
    <LoginButtons />
  </Layout>
)
