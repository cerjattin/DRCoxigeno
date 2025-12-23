export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#23C062",
        "primary-dark": "#1BA152",
        "accent-purple": "#7A00D2",
        "background-light": "#F9FBFA",
        "ox-dark": "#0F1A13",
        "ox-gray": "#54926D",
        "ox-border": "#D2E5D9",
      },
      boxShadow: {
        soft: "0 20px 60px rgba(0,0,0,0.10)",
      },
    },
  },
  plugins: [],
};
