import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (About.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../views/AboutView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
});

// Add a global beforeEach guard
router.beforeEach((to, from, next) => {
  const isPageReload = sessionStorage.getItem("isPageReload");
  sessionStorage.removeItem("isPageReload");

  if (isPageReload && to.fullPath !== "/") {
    next("/");
  } else {
    next();
  }
});

// Set a flag to detect page reload
window.addEventListener("beforeunload", () => {
  sessionStorage.setItem("isPageReload", "true");
});

export default router;
