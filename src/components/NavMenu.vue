<template>
  <div class="nav-float">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#fff"
      text-color="#303133"
      active-text-color="#409EFF"
      @select="handleSelect"
      router
    >
      <el-menu-item index="/">轨迹展示</el-menu-item>
      <el-menu-item index="/statistics">范围统计</el-menu-item>
      <el-menu-item index="density">车流密度</el-menu-item>
      <el-menu-item index="association">区域关联分析</el-menu-item>
      <el-menu-item index="frequency">频繁路径分析</el-menu-item>
      <el-menu-item index="/time">通时行间分析</el-menu-item>
      <el-menu-item index="/admin">
        <i class="el-icon-menu"></i>
        <span slot="title">登录信息</span>
      </el-menu-item>
    </el-menu>
    <div
      style="
        position: fixed;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        top: 24px;
        right: 32px;
        z-index: 9999;
        width: 35%;
      "
    >
      <el-select
        v-model="selectedOptions"
        multiple
        filterable
        placeholder="请选择"
        v-if="this.activeIndex === '/'"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-button
        type="primary"
        v-if="this.activeIndex === '/'"
        @click="handleSearch"
      >
        确定
      </el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "NavMenu",
  data() {
    return {
      activeIndex: this.$route.path,
      selectedOptions: [],
      options: [
        { value: "1", label: "选项1" },
        { value: "2", label: "选项2" },
        { value: "3", label: "选项3" },
      ],
    };
  },
  watch: {
    "$route.path"(newPath) {
      this.activeIndex = newPath;
    },
  },
  methods: {
    handleSelect(key) {
      this.activeIndex = key;
      this.$emit("menu-select", key);
    },
    handleSearch() {
      this.$emit("search", this.selectedOptions);
    },
  },
};
</script>

<style scoped>
.nav-float {
  position: fixed;
  top: 24px;
  left: 32px;
  z-index: 9999;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 6px;
}
.el-menu-demo {
  border-radius: 6px;
  min-width: 480px;
}
</style>
