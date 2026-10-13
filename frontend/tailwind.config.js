/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          main: "#171319",
          secondary: "#211A22",
          card: "#29212B",
          input: "#201921",
        },
        blush: {
          DEFAULT: "#E8A0B8",
          soft: "#F3C4D5",
          muted: "#B87591",
          subtle: "rgba(232, 160, 184, 0.12)",
        },
        cream: {
          DEFAULT: "#FFF7F2",
          muted: "#C5B8C1",
          subtle: "#8A7984",
        },
        border: {
          DEFAULT: "#493643",
          subtle: "rgba(73, 54, 67, 0.5)",
          strong: "#684E60",
        },
        brand: {
          DEFAULT: "#E8A0B8",
          hover: "#F3C4D5",
          dark: "#171319",
        },
        status: {
          genuine: "#52B788",
          warning: "#E0A96D",
          error: "#E05A68",
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(4px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
