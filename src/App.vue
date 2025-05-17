<template>
  <div id="app">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <router-view :key="this.$route.paths" id="router" />
    <map-view id="map" />
  </div>
</template>

<script>
import MapView from "./views/MapView.vue";
export default {
  name: "App",
  components: {
    MapView,
  },
  data() {
    return {};
  },
  methods: {},
  // watch: {
  //   selectedRoutes(newRoutes) {
  //     console.log("selectedRoutes", newRoutes);
  //   },
  // },
  //检测路由地址从statistics离开而做出相应的操作
  watch: {
    $route(to, from) {
      if (from.path === "/analysis") {
        if (this.$store.state.map.map) {
          this.$store.commit("RESET_MARKERLAYER");
        }
      }
    },
  },
};
</script>
<style>
html,
body {
  margin: 0;
  padding: 0;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  flex-direction: row-reverse;
  height: 100vh;
}
#map {
  flex-grow: 1;
  height: 100%;
  transition: width 0.3s ease-in-out;
  min-width: calc(100vw - 600px);
}
#router {
  width: 30%;
  height: 100%;
  background-color: white;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2000;
}
</style>
