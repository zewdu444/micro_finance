import { Typography } from '@mui/material'
import React from 'react'
import Link from '@mui/material/Link';
function CopyRight(props) {
  return (
    <Link color="inherit" href="https://portfolio-cpgd.onrender.com/"
    underline='none'
    target="_blank"
   >
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
    {'Copyright © '}

      Micro Finance
   {' '}
    {new Date().getFullYear()}
    {'.'}
  </Typography>
  </Link>
  )
}

export default CopyRight

