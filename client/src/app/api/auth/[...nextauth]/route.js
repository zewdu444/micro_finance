import NextAuth  from "next-auth/next";
import CredentialsProvider from "next-auth/providers/credentials";
import axios  from "axios";
import { redirect } from "next/dist/server/api-utils";
const handler= NextAuth({
    providers: [
        CredentialsProvider({
          // The name to display on the sign in form (e.g. "Sign in with...")
          name: "Credentials",
          // `credentials` is used to generate a form on the sign in page.
          // You can specify which fields should be submitted, by adding keys to the `credentials` object.
          // e.g. domain, username, password, 2FA token, etc.
          // You can pass any HTML attribute to the <input> tag through the object.
          credentials: {
            username: { label: "Username", type: "text", placeholder: "jsmith" },
            password: { label: "Password", type: "password" }
          },
          async authorize(credentials, req) {
            // Add logic here to look up the user from the credentials supplied
           const res = await fetch("http://localhost:8000/api/v1/users/login", {
              method: "POST",
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              body: new URLSearchParams({
                 "username": credentials?.username,
                 "password": credentials?.password
              })
           }).catch((error) => {
              console.log(error)
           })
            const user = res.data()
            if (user) {
                redirect("/")
              // Any object returned will be saved in `user` property of the JWT
              return user
            } else {
               console.log("check your details")
              // If you return null then an error will be displayed advising the user to check their details.
              return null

              // You can also Reject this callback with an Error thus the user will be sent to the error page with the error message as a query parameter
            }
          }
        })
      ],
      session: {
         strategy : "jwt",
      },
      callbacks: {
          async jwt(token, user, account, profile, isNewUser) {
            // Add access_token to the token right after signin
            if (user) {
               token.accessToken = user.accessToken
            }
            return token
          }
      }

})

export {handler as GET, handler as POST}
