import Vue from "vue";
import VueRouter from "vue-router";
import MapView from "../views/MapView.vue";
import AdminPanel from "../views/AdminPanel.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/map",
    name: "Map",
    component: MapView,
    // meta: { requiresAuth: true }
  },
  {
    path: "/",
    redirect: "/map",
  },
  {
    path: "/admin",
    name: "Admin",
    component: AdminPanel,
    // meta: { requiresAuth: true, requiresAdmin: true }
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
