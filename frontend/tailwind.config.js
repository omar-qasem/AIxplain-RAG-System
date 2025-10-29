/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'rag-green': '#00ff00',
        'rag-blue': '#00ffff',
      },
    },
  },
  plugins: [],
}
