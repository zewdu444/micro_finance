"use client"
import { useSession } from 'next-auth/react'
import React from 'react'
function Dashboard() {

  const {data:session, status} = useSession()
  console.log(session)
  if (status === 'loading') {
    return <div>Loading...</div>
  }
  if (status === "unauthenticated") {
    return <div>Access Denied</div>
  }

  return (

    <div>Dashboard
    {session.user.name}
    </div>
  )
}

export default Dashboard
