/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js, jsx, ts, tsx}"],
  theme: {
    extend: {
      colors: {
        "primary": "#becdd3",
        "secondary": "#5d439b",
      },
      fontSize: {
        "5.5xl": "3.5rem",
      }
    },
  },
  plugins: [],
}
