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
      <el-menu-item
        v-for="item in menuItems"
        :key="item.index"
        :index="item.index"
      >
        <i :class="item.icon" v-if="item.icon"></i>
        <span slot="title">{{ item.label }}</span>
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
          :key="item"
          :label="item"
          :value="item"
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
import axios from "axios";
export default {
  name: "NavMenu",
  data() {
    return {
      activeIndex: this.$route.path,
      selectedOptions: [],
      options: ["1", "2"], // 初始化选项为空
      menuItems: [
        { index: "/", label: "轨迹展示" },
        { index: "/statistics", label: "范围统计" },
        { index: "density", label: "车流密度" },
        { index: "association", label: "区域关联分析" },
        { index: "frequency", label: "频繁路径分析" },
        { index: "/time", label: "通时行间分析" },
        { index: "/admin", label: "登录信息", icon: "el-icon-menu" },
      ],
    };
  },
  mounted() {
    // 组件挂载后发起请求
    axios
      .get("/api/trailLists")
      .then((response) => {
        this.options = response.data;
      })
      .catch((error) => {
        console.error("获取轨迹列表失败:", error);
      });
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
