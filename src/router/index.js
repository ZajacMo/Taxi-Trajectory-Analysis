import Vue from "vue";
import VueRouter from "vue-router";
import AreaSearchView from "@/views/AreaSearchView.vue";
import DensityView from "@/views/DensityView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Map",
  },
  {
    path: "/statistics",
    name: "AreaStatistics",
    component: AreaSearchView,
  },
  {
    path: "/density",
    name: "Density",
    component: DensityView,
  },
  {
    path: "*",
    redirect: "/",
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
