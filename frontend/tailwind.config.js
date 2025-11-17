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
          100: "#00EEFF"
        },
        secondary: {
          50: "#ED7E00",
          // 100: "#FFC86E"
        },
        background: {
          50: "#030326",
          100: "#0C0220"
        }
      }
    }
  },
  plugins: [  
    require('tailwind-scrollbar-hide'),
  ],
}
