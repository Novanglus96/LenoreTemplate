import { defineStore } from "pinia";

export const useThemeStore = defineStore("theme", {
  state: () => ({
    currentTheme: localStorage.getItem("theme") || "myCustomLightTheme",
  }),
  actions: {
    setTheme(theme) {
      this.currentTheme = theme;
      localStorage.setItem("theme", theme);
    },
    toggleTheme() {
      const newTheme =
        this.currentTheme === "myCustomLightTheme"
          ? "myCustomDarkTheme"
          : "myCustomLightTheme";
      this.setTheme(newTheme);
    },
  },
});
