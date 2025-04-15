<template>
  <div>
    <el-menu
      :default-active="this.$route.path"
      class="el-menu-vertical-demo"
      :collapse="isCollapse"
      menu-trigger="click"
      router
    >
      <el-menu-item index="/map">
        <i class="el-icon-menu"></i>
        <span slot="title">地图</span>
      </el-menu-item>
      <el-menu-item index="/admin">
        <i class="el-icon-menu"></i>
        <span slot="title">管理</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "NavMenu",
  data() {
    return {
      isCollapse: false,
    };
  },
};
</script>

<style>
#menu {
  margin: 0 auto;
  max-width: 90%;
}
</style>
