
import ReduxProvider from "@/redux/provider"
import ThemeRegistry from '../../theme/ThemeRegistry'
import AuthProviders from "@/Providers"
export const metadata = {
  title: 'Micro finance management system',
  description: 'Micro finance management system',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
    <AuthProviders>
    <ReduxProvider>
     <ThemeRegistry>
      <body>
        {children}
      </body>
      </ThemeRegistry>
      </ReduxProvider>
      </AuthProviders>
    </html>
  )
}
