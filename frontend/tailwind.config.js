/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        titre: ["Belanosima", "sans-serif"],
        text: ["Nunito", "sans-serif"],
      },
      colors: {
        primary: {
          50: "#060444",
          100: "#3BBE78"
        },
        secondary: {
          50: "#C79B3B",
          // 100: "#FFC86E"
        },
        background: {
          50: "#16003B",
        }
      }
    }
  },
  plugins: [ 
    require('tailwind-scrollbar'),
    require('tailwind-scrollbar-hide'),
    require('@tailwindcss/typography'),
  ],
}
