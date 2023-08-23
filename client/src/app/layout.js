
import ReduxProvider from "@/redux/provider"
import ThemeRegistry from '../../theme/ThemeRegistry'
export const metadata = {
  title: 'Micro finance management system',
  description: 'Micro finance management system',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
    <ReduxProvider>
     <ThemeRegistry>
      <body>
        {children}
      </body>
      </ThemeRegistry>
      </ReduxProvider>
    </html>
  )
}
