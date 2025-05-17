<template>
  <div>
    <!-- 模式切换 -->
    <div>
      <h3 style="margin-top: 10px; margin-bottom: 10px">分析模式</h3>
      <el-select
        v-model="selected.mode"
        placeholder="请选择"
        style="margin-bottom: 10px"
      >
        <el-option
          v-for="item in options.selectOptions"
          :key="item"
          :label="item"
          :value="item"
        >
        </el-option>
      </el-select>
    </div>

    <!-- 区域数量切换 -->
    <div
      v-show="['区域关联分析', '频繁路径分析'].includes(selected.mode)"
      style="margin-top: 10px; margin-bottom: 10px"
    >
      <el-radio-group v-model="selected.radio">
        <el-radio-button label="单区域">
          <div v-if="selected.mode === '频繁路径分析'">全区域</div>
          <div v-else>单区域</div>
        </el-radio-button>
        <el-radio-button label="两区域">两区域</el-radio-button>
      </el-radio-group>
    </div>
  </div>
</template>
<script>
import { mapState } from "vuex";

export default {
  name: "ModeAndAreaSwitch",
  computed: {
    ...mapState(["map"]),
  },
  data() {
    return {
      options: {
        selectOptions: [
          "区域范围查找",
          "区域关联分析",
          "频繁路径分析",
          "通时行间分析",
        ],
      },
      selected: { radio: "单区域", mode: "区域范围查找" },
    };
  },
  watch: {
    selected: {
      handler(newVal) {
        this.$emit("select-change", newVal);
        // 在这里处理区域改变后的逻辑
      },
      deep: true,
    },
  },
};
</script>
<style scoped>
/* 可以添加样式 */
</style>
