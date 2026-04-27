/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#131314',
        surface: '#1c1b1c',
        primary: '#4F46E5', // Indigo vibrante
        secondary: '#00d16a', // Emerald para stats positivos
        textPrimary: '#e5e2e3',
        textSecondary: '#a1a1aa'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Newsreader', 'serif']
      }
    },
  },
  plugins: [],
}
