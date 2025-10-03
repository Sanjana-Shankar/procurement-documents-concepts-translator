/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}", // 👈 scans React components
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
