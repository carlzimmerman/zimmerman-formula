/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',  // Static export for Firebase hosting
  images: {
    unoptimized: true,  // Required for static export
  },
  trailingSlash: true,
}

module.exports = nextConfig
