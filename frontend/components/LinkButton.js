import React from 'react'
import Link from 'next/link'
import { Button } from 'semantic-ui-react'


class NavLink extends React.Component {

  render() {
    const { children, href, role, tabIndex, className } = this.props
    return (
      <Link href={href} prefetch>
        <a role={role} tabIndex={tabIndex} className={className}>
          {children}
        </a>
      </Link>
    )
  }

}

export default (props) => (
  <Button
    as={NavLink}
    {...props}
  />
)
