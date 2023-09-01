"use client"
import React from 'react'
import {SessionProvider} from "next-auth/react"
function AuthProviders({children}) {
  return (
    <SessionProvider>{children}</SessionProvider>
  )
}

export default AuthProviders
