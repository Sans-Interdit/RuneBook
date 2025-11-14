/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        titre: ["Belanosima", ""],
        text: ["Nunito", ""]
      },
      colors: {
        primary: {
          50: "#060444",
          100: "#00EEFF"
        },
        secondary: {
          50: "#ED7E00"
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
