import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import "@mdi/font/css/materialdesignicons.css";
import { VDateInput } from "vuetify/labs/VDateInput"; // Import the lab component

const myCustomLightTheme = {
  dark: false,
  colors: {
    primary: "#8c0c0c",
    secondary: "#FBF4F4",
    accent: "#671209",
    error: "#FF3407",
    warning: "#ffc107",
    info: "#795548",
    success: "#4caf50",
    selected: "#7fb17f",
    surface: "#ECFDF5",
    background: "#F5F5F5",
    textPending: "#EFFDF6",
    textCleared: "#1D1D35",
    bgPending: "#E0E0E0",
    altAccent: "#D95D3B",
    "on-background": "#212121",
    "on-surface": "#212121",
  },
};

const myCustomDarkTheme = {
  dark: true,
  colors: {
    primary: "#06966A",
    secondary: "#b3c7bd",
    accent: "#FF784E",
    error: "#CF6679",
    warning: "#ffc107",
    info: "#2196F3",
    success: "#4CAF50",
    selected: "#A5D6A7",
    surface: "#212121",
    background: "#121212",
    textPending: "#1D1D35",
    textCleared: "#EFFDF6",
    bgPending: "#3D3D3D",
    altAccent: "#D4f$FF",
    "on-background": "#ffffff",
    "on-surface": "#ffffff",
  },
};

export default createVuetify({
  theme: {
    defaultTheme: "myCustomLightTheme",
    variations: {
      colors: ["primary", "secondary", "accent"],
      lighten: 3,
      darken: 3,
    },
    themes: {
      myCustomLightTheme,
      myCustomDarkTheme,
    },
  },
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
  components: {
    ...components, // Spread the default Vuetify components
    VDateInput, // Add the lab component
  },
  directives,
});
