import { Typography } from '@mui/material'
import React from 'react'
import Link from '@mui/material/Link';
function CopyRight(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
    {'Copyright © '}
    <Link color="inherit" href="https://portfolio-cpgd.onrender.com/"
     underline='none'
    >
      Micro Finance
    </Link>{' '}
    {new Date().getFullYear()}
    {'.'}
  </Typography>
  )
}

export default CopyRight

