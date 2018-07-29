import Head from 'next/head'
import { Container } from 'semantic-ui-react'

const globalCSS = `
  html {
    -ms-touch-action: manipulation;
    touch-action: manipulation;
  }
  h1 {
    margin-top: 1rem;
    margin-bottom: 1rem;
  }

`

export default ({ children, title }) => (
  <div style={{ paddingTop: 20 }}>
    <Head>
      <title>{title || 'Chat'}</title>
      <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1, shrink-to-fit=no" />
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.3.1/semantic.min.css" />
      <style>{globalCSS}</style>
    </Head>
    <Container text>
      {children}
    </Container>
  </div>
)
