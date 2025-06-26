/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      // Custom CSS variables for dark theme consistency
      colors: {
        'hero-overlay': 'rgba(15, 15, 16, 0.85)',
      }
    }
  },
  daisyui: {
    themes: ["dark"], // Only dark theme as requested
    darkTheme: "dark",
    base: true,
    styled: true,
    utils: true,
    prefix: "",
    logs: false, // Disable logs for cleaner output
  },
  plugins: [require("daisyui")]
}