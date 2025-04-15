<template>
  <div id="app">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <el-row>
      <el-col :span="3">
        <nav-menu></nav-menu>
      </el-col>
      <el-col :span="21">
        <router-view :key="this.$route.paths"></router-view>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import NavMenu from "./components/NavMenu.vue";
export default {
  name: "App",
  components: {
    NavMenu,
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.bg-purple {
  background: #d3dce6;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
