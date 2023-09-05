"use client"
import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { signIn } from 'next-auth/react';
import { useRouter } from "next/navigation"
import Alert from '@mui/material/Alert';
import { useState } from 'react';
import CopyRight from '../components/CopyRight';


export default function Login() {
  const [open, setOpen] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter()
  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const res = await signIn('credentials', {
      username: data.get('username'),
      password: data.get('password'),
      redirect: false,
    })
    if (res.error === "Invalid credentials") {
      setOpen(true)
       // Use setTimeout to set open back to false after 3 seconds
     setError("The username or password you entered is incorrect")
     setTimeout(() => {
     setOpen(false);
     }, 3000); // 3000 milliseconds = 3 seconds

    }
    if(res.error === "fetch failed") {
      setOpen(true)
      // Use setTimeout to set open back to false after 3 seconds
    setError("Network Error")
    setTimeout(() => {
    setOpen(false);
    }, 3000); // 3000 milliseconds = 3 seconds
    }
     if(res.ok && res.url) {
      router.push("/dashboard")
     }


  };

  return (

      <Container component="main" maxWidth="xs">
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Alert
          sx = {{display: open ? "inline-flex" : "none"}}
          severity="error">{error}</Alert>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                <Link href="/auth/resetbyemail" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link href="/auth/register" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <CopyRight sx={{ mt: 8, mb: 4 }} />
      </Container>
  );
  }
