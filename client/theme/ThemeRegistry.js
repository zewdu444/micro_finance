"use client"
import {createTheme, ThemeProvider} from '@mui/material/styles'
import  CssBaseline  from '@mui/material/CssBaseline'
import { useSelector } from 'react-redux';
export  default function ThemeRegistry({children}) {
  const theme =useSelector((state)=>state.themes.mode)
  const Theme = createTheme({
    typography: {
      fontFamily: [
        'Lato', 'sans-serif',
      ].join(','),
    },
    palette: {
      background: {
        default: theme === 'light' ? '#F7F9FC' : '#002412',
        paper: theme === 'light' ? '#fff' : '#00140a',
      },
      primary: {
        light: '#e3fdf9',
        main: '#00ab55',
        dark: '#002884',
        contrastText: '#fff',
      },
      secondary: {
        light: '#e3fdf9',
        main: '#f50057',
        dark: '#ba000d',
        contrastText: '#000',
      },
      mode: theme,
    },
    components: {
      MuiAppBar:{
         styleOverrides:{
          root:{
            backgroundColor: theme ==='light' ? 'white' :'#002412',
            color: theme=== 'light' ? '#00ab55' :'white',
            border: '1px solid',
            borderColor:theme ==='light' ? 'white' :'#002412',
            borderRadius :'10px'
          }
         }
      }

    }

  });


  return (
    <ThemeProvider theme={Theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  )
}
