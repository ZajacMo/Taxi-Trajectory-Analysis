import Vue from "vue";
import VueRouter from "vue-router";
import AreaSearchDialog from "@/components/AreaSearchDialog.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Map",
  },
  {
    path: "/statistics",
    name: "AreaStatistics",
    component: AreaSearchDialog,
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
