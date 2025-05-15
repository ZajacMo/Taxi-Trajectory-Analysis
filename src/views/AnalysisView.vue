<template>
  <div class="association-view">
    <!-- 模式和区域切换 -->
    <ModeAndAreaSwitch @select-change="(newVal) => (selected = newVal)" />

    <!-- 频繁路径分析 -->
    <Frequenc-view v-if="selected.mode === '频繁路径分析'" />

    <!-- 区域1坐标 -->
    <div
      v-show="selected.mode !== '频繁路径分析' || selected.radio !== '单区域'"
    >
      <el-divider>
        <h3
          v-if="
            (selected.radio === '两区域' &&
              ['区域关联分析', '频繁路径分析'].includes(selected.mode)) ||
            selected.mode === '通时行间分析'
          "
        >
          区域1
        </h3>
        <h3 v-else>区域</h3>
      </el-divider>
      <select-rectangle @area-change="handleArea1Change" />
    </div>

    <!-- 区域2坐标 -->
    <div
      v-show="
        (selected.radio === '两区域' &&
          ['区域关联分析', '频繁路径分析'].includes(selected.mode)) ||
        selected.mode === '通时行间分析'
      "
    >
      <el-divider><h3>区域2</h3></el-divider>
      <select-rectangle @area-change="handleArea2Change" />
    </div>

    <!-- 时间选择器 -->
    <el-time-picker
      v-if="selected.mode === '区域范围查找'"
      v-model="timeRange"
      is-range
      range-separator="至"
      start-placeholder="开始时间"
      end-placeholder="结束时间"
      size="medium"
    ></el-time-picker>

    <div style="padding-top: 20px">
      <el-button type="danger" @click="clearAll">清空</el-button>
      <el-button type="primary" @click="confirm">确认</el-button>
    </div>
  </div>
</template>
<script>
import { mapState } from "vuex";
import SelectRectangle from "@/components/SelectRectangle.vue";
import FrequencView from "@/components/FrequencView.vue";
import ModeAndAreaSwitch from "@/components/ModeAndAreaSwitch.vue";
export default {
  name: "AnalysisView",
  components: {
    SelectRectangle,
    FrequencView,
    ModeAndAreaSwitch,
  },
  computed: {
    ...mapState(["map"]),
  },
  data() {
    return {
      // radio: "单区域",
      // selectedMode: "区域范围查找",
      selected: {
        radio: "单区域",
        mode: "区域范围查找",
      },
      radioList: ["单区域", "两区域"],
      selectList: [
        "区域范围查找",
        "区域关联分析",
        "频繁路径分析",
        "通时行间分析",
      ],
      timeRange: [],
    };
  },
  methods: {
    handleArea1Change(newVal) {
      console.log("area1 changed", newVal);
      // 在这里处理区域改变后的逻辑
    },
    handleArea2Change(newVal) {
      console.log("area2 changed", newVal);
      // 在这里处理区域改变后的逻辑
    },
    clearAll() {
      // 清空所有区域
      // this.$store.commit("RESET_MARKERLAYER");
    },
    confirm() {
      // 确认按钮点击事件
      // 在这里处理确认按钮的逻辑
    },
  },
};
</script>
<style>
.el-input {
  padding-right: 20px;
}
.association-view {
  padding: 40px;
  padding-top: 0;
}
h3 {
  margin: 0;
}
h4 {
  margin: 0;
}
</style>
