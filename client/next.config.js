/** @type {import('next').NextConfig} */
const nextConfig = {
  swcMinify: true,
  modularizeImports: {
    "@mui/icons-material": {
       transform: "@mui/icons-material/${member}",
    }
  }
}

module.exports = nextConfig
