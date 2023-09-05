import NextAuth  from "next-auth/next";
import CredentialsProvider from "next-auth/providers/credentials";
import axios  from "axios";
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
           })
           const user = await res.json();
           if (!res.ok) {
              throw new Error("Invalid credentials");
            }

            if (res.ok && user) {

              return user;
            }
            return null
          }
        })
      ],
      secret: process.env.NEXTAUTH_SECRET,
      session: {
         strategy : "jwt",
      },
      pages: {
        signIn: 'auth/login',
      },
      callbacks: {
        async jwt({ token, user, account }) {
          if (account && user) {
            return {
              ...token,
              accessToken: user.token,
              refreshToken: user.refreshToken,
            };
          }

          return token;
        },
        },
        async session({ session, token }) {
          session.user.accessToken = token.accessToken;
          session.user.refreshToken = token.refreshToken;
          session.user.accessTokenExpires = token.accessTokenExpires;

          return session;
        },
      debug: process.env.NODE_ENV === 'development',

})

export {handler as GET, handler as POST}
