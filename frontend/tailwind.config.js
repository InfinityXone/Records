/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'primary-cyan': '#00FFFF', // cyan accent
        'primary-lime': '#A7F432', // neon lime green
        'primary-blue': '#1E90FF', // neon blue
        'glass-dark': 'rgba(0, 0, 0, 0.6)',
        'glass-light': 'rgba(255, 255, 255, 0.1)',
      },
    },
  },
  plugins: [],
};
