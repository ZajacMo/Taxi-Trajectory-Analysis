import Vue from "vue";
import VueRouter from "vue-router";
import DensityView from "@/views/DensityView.vue";
import AnalysisView from "@/views/AnalysisView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Map",
  },
  {
    path: "/density",
    name: "Density",
    component: DensityView,
  },
  {
    path: "/analysis",
    name: "Analysis",
    component: AnalysisView,
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
